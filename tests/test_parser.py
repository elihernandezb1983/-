"""Тесты парсера сообщений о войнах."""

from __future__ import annotations

import unittest

from war.parser import WarEventKind, is_war_message, normalize_tg_text, parse_war_message


class WarParserTests(unittest.TestCase):
    def test_attack_declare(self) -> None:
        text = (
            "Организация: события\n"
            "Ваша организация забила Ag. Blade войну за Нефть на 18:30, 5x5, без аптечек."
        )
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.ATTACK_DECLARE)
        self.assertEqual(event.opponent, "Ag. Blade")
        self.assertEqual(event.location, "Нефть")
        self.assertEqual(event.time, "18:30")
        self.assertEqual(event.format, "5x5")
        self.assertEqual(event.conditions, "без аптечек")

    def test_defense_declare(self) -> None:
        text = "Ag. Blade забили Вашей организации войну за Порт Биз на 20:00, 3x3"
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.DEFENSE_DECLARE)
        self.assertEqual(event.opponent, "Ag. Blade")
        self.assertEqual(event.location, "Порт Биз")

    def test_attack_win(self) -> None:
        text = "Захватывает Нефть в бою #12345"
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.ATTACK_WIN)
        self.assertEqual(event.location, "Нефть")
        self.assertEqual(event.battle_id, 12345)

    def test_defense_win(self) -> None:
        text = "Удерживают Стройка в бою #99"
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.DEFENSE_WIN)
        self.assertEqual(event.location, "Стройка")
        self.assertEqual(event.battle_id, 99)

    def test_loss_with_battle_id(self) -> None:
        text = "Проигрывает в бою #777 за Мясо."
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.LOSS)
        self.assertEqual(event.battle_id, 777)
        self.assertEqual(event.location, "Мясо")

    def test_loss_without_battle_id(self) -> None:
        text = "Проигрывает Мясо."
        event = parse_war_message(text)
        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event.kind, WarEventKind.LOSS)
        self.assertIsNone(event.battle_id)
        self.assertEqual(event.location, "Мясо")

    def test_normalize_cyrillic_x(self) -> None:
        self.assertEqual(normalize_tg_text("5х5"), "5x5")

    def test_non_war_message(self) -> None:
        self.assertIsNone(parse_war_message("Обычное сообщение в чате"))
        self.assertFalse(is_war_message("Привет"))


if __name__ == "__main__":
    unittest.main()
