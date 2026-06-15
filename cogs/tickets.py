from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

import config
import storage
from audit_log import log_usage_from_interaction
from cogs.panel import _can_use_panel


def _format_roles(guild: discord.Guild, role_ids: list[int]) -> str:
    if not role_ids:
        return "— (роли не заданы)"
    lines = []
    for rid in role_ids:
        role = guild.get_role(rid)
        lines.append(role.mention if role else f"`{rid}` (удалена)")
    return "\n".join(lines)


class TicketsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def _deny(self, interaction: discord.Interaction) -> bool:
        if _can_use_panel(interaction):
            return False
        await interaction.response.send_message(
            config.MESSAGES["no_permission"],
            ephemeral=True,
        )
        return True

    @app_commands.command(
        name="тикет-настройка",
        description="Настройка тикетов заявок в семью",
    )
    @app_commands.describe(
        действие="Что сделать",
        категория="Категория для каналов ticket-0001 (для действия «Категория»)",
        роль="Роль (для действий с ролями)",
    )
    @app_commands.choices(
        действие=[
            app_commands.Choice(
                name="Категория для тикетов",
                value="category",
            ),
            app_commands.Choice(
                name="Роль просмотра — добавить",
                value="staff_add",
            ),
            app_commands.Choice(
                name="Роль просмотра — удалить",
                value="staff_remove",
            ),
            app_commands.Choice(
                name="Роль при принятии заявки",
                value="accepted",
            ),
            app_commands.Choice(
                name="Показать все настройки",
                value="list",
            ),
        ],
    )
    async def ticket_setup(
        self,
        interaction: discord.Interaction,
        действие: app_commands.Choice[str],
        категория: discord.CategoryChannel | None = None,
        роль: discord.Role | None = None,
    ) -> None:
        if await self._deny(interaction):
            return
        if not interaction.guild:
            return

        action = действие.value

        if action == "category":
            if категория is None:
                await interaction.response.send_message(
                    config.MESSAGES["ticket_setup_need_category"],
                    ephemeral=True,
                )
                return
            storage.update_guild(
                interaction.guild.id,
                ticket_category_id=категория.id,
            )
            log_usage_from_interaction(
                interaction,
                "ticket.settings.category",
                details={"category_id": категория.id, "category_name": категория.name},
                bot=self.bot,  # type: ignore[arg-type]
            )
            await interaction.response.send_message(
                config.MESSAGES["ticket_category_set"].format(category=категория.mention),
                ephemeral=True,
            )
            return

        if action in ("staff_add", "staff_remove", "accepted"):
            if роль is None:
                await interaction.response.send_message(
                    config.MESSAGES["ticket_setup_need_role"],
                    ephemeral=True,
                )
                return

        if action == "staff_add":
            guild_data = storage.get_guild(interaction.guild.id)
            ids: list[int] = list(guild_data.get("staff_role_ids") or [])
            if роль.id in ids:
                await interaction.response.send_message(
                    config.MESSAGES["ticket_role_exists"].format(role=роль.mention),
                    ephemeral=True,
                )
                return
            ids.append(роль.id)
            storage.update_guild(interaction.guild.id, staff_role_ids=ids)
            log_usage_from_interaction(
                interaction,
                "ticket.settings.staff_add",
                details={"role_id": роль.id, "role_name": роль.name},
                bot=self.bot,  # type: ignore[arg-type]
            )
            await interaction.response.send_message(
                config.MESSAGES["ticket_role_added"].format(role=роль.mention),
                ephemeral=True,
            )
            return

        if action == "staff_remove":
            guild_data = storage.get_guild(interaction.guild.id)
            ids: list[int] = list(guild_data.get("staff_role_ids") or [])
            if роль.id not in ids:
                await interaction.response.send_message(
                    config.MESSAGES["ticket_role_missing"].format(role=роль.mention),
                    ephemeral=True,
                )
                return
            ids.remove(роль.id)
            storage.update_guild(interaction.guild.id, staff_role_ids=ids)
            log_usage_from_interaction(
                interaction,
                "ticket.settings.staff_remove",
                details={"role_id": роль.id, "role_name": роль.name},
                bot=self.bot,  # type: ignore[arg-type]
            )
            await interaction.response.send_message(
                config.MESSAGES["ticket_role_removed"].format(role=роль.mention),
                ephemeral=True,
            )
            return

        if action == "accepted":
            storage.update_guild(interaction.guild.id, accepted_role_id=роль.id)
            log_usage_from_interaction(
                interaction,
                "ticket.settings.accepted_role",
                details={"role_id": роль.id, "role_name": роль.name},
                bot=self.bot,  # type: ignore[arg-type]
            )
            await interaction.response.send_message(
                config.MESSAGES["ticket_accepted_role_set"].format(role=роль.mention),
                ephemeral=True,
            )
            return

        # list
        guild_data = storage.get_guild(interaction.guild.id)
        category_id = guild_data.get("ticket_category_id")
        category = (
            interaction.guild.get_channel(category_id)
            if category_id
            else None
        )
        cat_text = (
            category.mention
            if isinstance(category, discord.CategoryChannel)
            else "— (не задана)"
        )

        accepted_id = guild_data.get("accepted_role_id")
        accepted_role = (
            interaction.guild.get_role(accepted_id) if accepted_id else None
        )
        accepted_text = accepted_role.mention if accepted_role else "— (не задана)"

        await interaction.response.send_message(
            config.MESSAGES["ticket_settings_summary"].format(
                category=cat_text,
                roles=_format_roles(
                    interaction.guild,
                    guild_data.get("staff_role_ids") or [],
                ),
                accepted_role=accepted_text,
                next_number=guild_data.get("next_ticket_number", 1),
            ),
            ephemeral=True,
        )

