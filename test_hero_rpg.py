"""
test_hero_rpg.py
================
Pytest test suite for the Hero Quest RPG project.
Run with:  pytest -v test_hero_rpg.py

Tests cover:
  - Bag[T] generic container (all methods)
  - Hero constructor defaults
  - Combat methods (take_damage, heal, is_alive)
  - Weapon equipping and damage potential
  - Skill learning (set behavior)
  - Inventory pick-up and defaultdict grouping
  - Kill tracking with Counter
  - Combat log with deque (maxlen)
  - Stat upgrades
"""

import pytest
from collections import Counter, defaultdict, deque
from hero_rpg import Hero, Weapon, Item, Bag, WeaponType, ItemType


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES  — reusable test data
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def hero() -> Hero:
    """A fresh Warrior hero for each test."""
    return Hero("Aric", "Warrior", max_health=100)


@pytest.fixture
def sword() -> Weapon:
    return Weapon("Iron Sword", WeaponType.SWORD, damage=30)


@pytest.fixture
def dagger() -> Weapon:
    return Weapon("Shadow Dagger", WeaponType.DAGGER, damage=18)


@pytest.fixture
def bow() -> Weapon:
    return Weapon("Elven Bow", WeaponType.BOW, damage=22)


@pytest.fixture
def potion() -> Item:
    return Item("Health Potion", ItemType.POTION, value=50)


@pytest.fixture
def armor() -> Item:
    return Item("Iron Shield", ItemType.ARMOR, value=120)


# ══════════════════════════════════════════════════════════════════════════════
# BAG[T] TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestBag:
    """Tests for the generic Bag[T] container."""

    def test_bag_starts_empty(self):
        """A new bag should have zero items."""
        bag: Bag[str] = Bag(capacity=5)
        assert len(bag) == 0

    def test_add_returns_true_when_space_available(self):
        """add() should return True and increase length by 1."""
        bag: Bag[str] = Bag(capacity=5)
        result = bag.add("item_a")
        assert result is True
        assert len(bag) == 1

    def test_add_returns_false_when_full(self):
        """add() should return False and not change length when at capacity."""
        bag: Bag[int] = Bag(capacity=2)
        bag.add(1)
        bag.add(2)
        # Bag is now full
        result = bag.add(3)
        assert result is False
        assert len(bag) == 2

    def test_is_full_false_when_space_remains(self):
        bag: Bag[str] = Bag(capacity=3)
        bag.add("x")
        assert bag.is_full() is False

    def test_is_full_true_at_capacity(self):
        bag: Bag[str] = Bag(capacity=2)
        bag.add("x")
        bag.add("y")
        assert bag.is_full() is True

    def test_remove_existing_item(self):
        """remove() should return True and reduce length by 1."""
        bag: Bag[str] = Bag(capacity=5)
        bag.add("sword")
        result = bag.remove("sword")
        assert result is True
        assert len(bag) == 0

    def test_remove_nonexistent_item_returns_false(self):
        """remove() should return False if the item is not in the bag."""
        bag: Bag[str] = Bag(capacity=5)
        result = bag.remove("ghost_item")
        assert result is False

    def test_all_returns_copy_not_reference(self):
        """all() must return a copy so external mutation doesn't affect bag."""
        bag: Bag[str] = Bag(capacity=5)
        bag.add("a")
        copy = bag.all()
        copy.append("injected")         # mutate the copy
        assert len(bag) == 1            # internal bag must be unchanged

    def test_bag_preserves_insertion_order(self):
        """Items should be returned in insertion order (list-backed)."""
        bag: Bag[str] = Bag(capacity=5)
        for ch in ["c", "a", "b"]:
            bag.add(ch)
        assert bag.all() == ["c", "a", "b"]

    def test_bag_generic_with_weapon_type(self, sword, dagger):
        """Verify Bag works correctly when typed as Bag[Weapon]."""
        bag: Bag[Weapon] = Bag(capacity=2)
        bag.add(sword)
        bag.add(dagger)
        assert len(bag) == 2
        assert sword in bag.all()


# ══════════════════════════════════════════════════════════════════════════════
# HERO CONSTRUCTOR TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestHeroConstructor:
    """Verify that the Hero is initialized with the correct defaults."""

    def test_hero_name_and_class(self, hero):
        assert hero.name == "Aric"
        assert hero.hero_class == "Warrior"

    def test_health_starts_at_max(self, hero):
        """health should equal max_health on creation."""
        assert hero.health == hero.max_health == 100

    def test_inventory_is_bag_of_item(self, hero):
        """inventory should be a Bag with capacity 20 and zero items."""
        assert isinstance(hero.inventory, Bag)
        assert hero.inventory.capacity == 20
        assert len(hero.inventory) == 0

    def test_equipped_weapons_is_bag_with_capacity_3(self, hero):
        assert isinstance(hero.equipped_weapons, Bag)
        assert hero.equipped_weapons.capacity == 3

    def test_skills_is_empty_set(self, hero):
        """skills must be a set (not list or dict)."""
        assert isinstance(hero.skills, set)
        assert len(hero.skills) == 0

    def test_stats_has_correct_default_values(self, hero):
        """Default stats should match the spec exactly."""
        assert hero.stats["strength"]     == 10
        assert hero.stats["dexterity"]    == 10
        assert hero.stats["intelligence"] == 10
        assert hero.stats["defense"]      == 5

    def test_kill_counter_is_counter(self, hero):
        assert isinstance(hero.kill_counter, Counter)

    def test_item_registry_is_defaultdict(self, hero):
        assert isinstance(hero._item_registry, defaultdict)

    def test_combat_log_is_deque_with_maxlen_10(self, hero):
        """combat_log must be a deque with maxlen=10."""
        assert isinstance(hero.combat_log, deque)
        assert hero.combat_log.maxlen == 10


# # ══════════════════════════════════════════════════════════════════════════════
# # COMBAT TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestCombat:
#     """Tests for take_damage, heal, and is_alive."""

#     def test_take_damage_reduces_health(self, hero):
#         hero.take_damage(30)
#         assert hero.health == 70

#     def test_take_damage_returns_actual_damage(self, hero):
#         returned = hero.take_damage(30)
#         assert returned == 30

#     def test_take_damage_capped_at_current_health(self, hero):
#         """Overkill damage should clamp to current HP, not go negative."""
#         returned = hero.take_damage(200)   # hero only has 100 HP
#         assert returned == 100             # actual damage = full HP
#         assert hero.health == 0

#     def test_health_never_goes_below_zero(self, hero):
#         hero.take_damage(9999)
#         assert hero.health == 0

#     def test_is_alive_true_with_health(self, hero):
#         assert hero.is_alive() is True

#     def test_is_alive_false_when_health_zero(self, hero):
#         hero.take_damage(100)
#         assert hero.is_alive() is False

#     def test_heal_increases_health(self, hero):
#         hero.take_damage(40)
#         hero.heal(20)
#         assert hero.health == 80

#     def test_heal_returns_actual_hp_restored(self, hero):
#         hero.take_damage(40)
#         restored = hero.heal(20)
#         assert restored == 20

#     def test_heal_capped_at_max_health(self, hero):
#         """Healing beyond max_health should clamp to max_health."""
#         hero.take_damage(10)
#         restored = hero.heal(9999)
#         assert restored == 10            # only 10 HP was missing
#         assert hero.health == hero.max_health

#     def test_take_damage_adds_to_combat_log(self, hero):
#         hero.take_damage(25)
#         assert any("took 25 damage" in entry for entry in hero.combat_log)

#     def test_heal_adds_to_combat_log(self, hero):
#         hero.take_damage(50)
#         hero.heal(20)
#         assert any("healed 20 HP" in entry for entry in hero.combat_log)

#     def test_combat_log_rolls_over_at_10_entries(self, hero):
#         """deque(maxlen=10) must drop the oldest entry at the 11th event."""
#         for i in range(11):
#             hero.take_damage(1)
#         assert len(hero.combat_log) == 10


# # ══════════════════════════════════════════════════════════════════════════════
# # WEAPON TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestWeapons:
#     """Tests for equipping weapons and damage potential."""

#     def test_equip_weapon_returns_true(self, hero, sword):
#         assert hero.equip_weapon(sword) is True

#     def test_equip_weapon_adds_to_equipped(self, hero, sword):
#         hero.equip_weapon(sword)
#         assert sword in hero.equipped_weapons.all()

#     def test_equip_weapon_fails_when_slots_full(self, hero, sword, dagger, bow):
#         hero.equip_weapon(sword)
#         hero.equip_weapon(dagger)
#         hero.equip_weapon(bow)
#         extra = Weapon("Battle Axe", WeaponType.SWORD, damage=40)
#         result = hero.equip_weapon(extra)
#         assert result is False

#     def test_total_damage_potential_sums_equipped_weapons(self, hero, sword, dagger):
#         hero.equip_weapon(sword)   # 30
#         hero.equip_weapon(dagger)  # 18
#         assert hero.total_damage_potential() == 48

#     def test_total_damage_potential_zero_with_no_weapons(self, hero):
#         assert hero.total_damage_potential() == 0

#     def test_equip_weapon_logs_event(self, hero, sword):
#         hero.equip_weapon(sword)
#         assert any("Iron Sword" in entry for entry in hero.combat_log)


# # ══════════════════════════════════════════════════════════════════════════════
# # SKILL TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestSkills:
#     """Tests verifying set behavior for skill learning."""

#     def test_learn_new_skill_returns_true(self, hero):
#         assert hero.learn_skill("Shield Bash") is True

#     def test_learn_duplicate_skill_returns_false(self, hero):
#         hero.learn_skill("Shield Bash")
#         result = hero.learn_skill("Shield Bash")   # duplicate
#         assert result is False

#     def test_skills_set_contains_no_duplicates(self, hero):
#         hero.learn_skill("Fireball")
#         hero.learn_skill("Fireball")
#         hero.learn_skill("Fireball")
#         assert len(hero.skills) == 1   # set: no duplicates

#     def test_skills_is_unordered_set(self, hero):
#         hero.learn_skill("A")
#         hero.learn_skill("B")
#         hero.learn_skill("C")
#         # The collection is a set, not a list
#         assert isinstance(hero.skills, set)

#     def test_multiple_different_skills(self, hero):
#         hero.learn_skill("Dodge")
#         hero.learn_skill("Counter Strike")
#         hero.learn_skill("War Cry")
#         assert "Dodge" in hero.skills
#         assert "War Cry" in hero.skills
#         assert len(hero.skills) == 3


# # ══════════════════════════════════════════════════════════════════════════════
# # INVENTORY TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestInventory:
#     """Tests for item pick-up and defaultdict grouping."""

#     def test_pick_up_item_returns_true(self, hero, potion):
#         assert hero.pick_up_item(potion) is True

#     def test_pick_up_item_adds_to_inventory(self, hero, potion):
#         hero.pick_up_item(potion)
#         assert potion in hero.inventory.all()

#     def test_pick_up_item_registers_by_type(self, hero, potion, armor):
#         hero.pick_up_item(potion)
#         hero.pick_up_item(armor)
#         grouped = hero.items_by_type()
#         # potion should be under "Potion" key
#         assert "Potion" in grouped
#         assert potion in grouped["Potion"]
#         # armor should be under "Armor" key
#         assert "Armor" in grouped
#         assert armor in grouped["Armor"]

#     def test_multiple_potions_grouped_together(self, hero):
#         p1 = Item("Health Potion", ItemType.POTION, value=50)
#         p2 = Item("Mana Potion",   ItemType.POTION, value=40)
#         hero.pick_up_item(p1)
#         hero.pick_up_item(p2)
#         grouped = hero.items_by_type()
#         assert len(grouped["Potion"]) == 2

#     def test_items_by_type_returns_plain_dict(self, hero, potion):
#         hero.pick_up_item(potion)
#         result = hero.items_by_type()
#         # Should be a regular dict, not a defaultdict
#         assert type(result) is dict

#     def test_pick_up_returns_false_when_full(self, hero):
#         """inventory capacity is 20; adding a 21st item should fail."""
#         for i in range(20):
#             hero.pick_up_item(Item(f"Item_{i}", ItemType.MISC, value=1))
#         extra = Item("One Too Many", ItemType.MISC, value=1)
#         assert hero.pick_up_item(extra) is False


# # ══════════════════════════════════════════════════════════════════════════════
# # KILL COUNTER TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestKillCounter:
#     """Tests for Counter-based kill tracking."""

#     def test_record_kill_increments_counter(self, hero):
#         hero.record_kill("Goblin")
#         assert hero.kill_counter["Goblin"] == 1

#     def test_record_kill_accumulates(self, hero):
#         for _ in range(5):
#             hero.record_kill("Goblin")
#         assert hero.kill_counter["Goblin"] == 5

#     def test_top_kills_returns_most_common(self, hero):
#         for _ in range(5): hero.record_kill("Goblin")
#         for _ in range(3): hero.record_kill("Orc")
#         hero.record_kill("Dragon")
#         top = hero.top_kills(2)
#         assert top[0] == ("Goblin", 5)
#         assert top[1] == ("Orc", 3)

#     def test_top_kills_default_n_is_3(self, hero):
#         hero.record_kill("A")
#         hero.record_kill("B")
#         hero.record_kill("C")
#         hero.record_kill("D")
#         assert len(hero.top_kills()) == 3

#     def test_record_kill_adds_to_combat_log(self, hero):
#         hero.record_kill("Troll")
#         assert any("Troll" in entry for entry in hero.combat_log)

#     def test_kill_counter_unknown_enemy_returns_zero(self, hero):
#         """Counter defaults missing keys to 0 — no KeyError."""
#         assert hero.kill_counter["Unknown"] == 0


# # ══════════════════════════════════════════════════════════════════════════════
# # STAT UPGRADE TESTS
# # ══════════════════════════════════════════════════════════════════════════════

# class TestStats:
#     """Tests for upgrading hero stats."""

#     def test_upgrade_existing_stat(self, hero):
#         result = hero.upgrade_stat("strength", 5)
#         assert result is True
#         assert hero.stats["strength"] == 15

#     def test_upgrade_nonexistent_stat_returns_false(self, hero):
#         result = hero.upgrade_stat("luck", 10)
#         assert result is False

#     def test_upgrade_does_not_affect_other_stats(self, hero):
#         hero.upgrade_stat("strength", 10)
#         assert hero.stats["dexterity"] == 10    # unchanged
#         assert hero.stats["defense"]   == 5     # unchanged

#     def test_multiple_upgrades_accumulate(self, hero):
#         hero.upgrade_stat("intelligence", 5)
#         hero.upgrade_stat("intelligence", 5)
#         assert hero.stats["intelligence"] == 20
