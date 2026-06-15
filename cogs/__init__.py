from .audit import AuditCog
from .panel import PanelCog
from .tickets import TicketsCog
from .war import WarCog


async def setup(bot):
    await bot.add_cog(AuditCog(bot))
    await bot.add_cog(PanelCog(bot))
    await bot.add_cog(TicketsCog(bot))
    await bot.add_cog(WarCog(bot))
