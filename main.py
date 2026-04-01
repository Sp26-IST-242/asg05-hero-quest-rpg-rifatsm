"""
main.py
=======
Demo for the Hero Quest RPG.
Run with:  python main.py

Demonstrates the complete Hero system:
  - Creating a hero
  - Equipping weapons
  - Learning skills (set uniqueness)
  - Picking up items (defaultdict grouping)
  - Taking damage and healing (clamping logic)
  - Recording kills (Counter)
  - Viewing the rolling combat log (deque)
  - Upgrading stats (dict)
"""

from hero_rpg import Hero, Weapon, Item, WeaponType, ItemType


def main() -> None:
    # ── Create hero ───────────────────────────────────────────────────────────
    hero = Hero("Aric", "Warrior", max_health=120)
    # print(hero)

    # ── Equip weapons (Bag[Weapon], capacity 3) ───────────────────────────────
    sword  = Weapon("Iron Sword",    WeaponType.SWORD,  damage=30)
    dagger = Weapon("Shadow Dagger", WeaponType.DAGGER, damage=18)
    bow    = Weapon("Elven Bow",     WeaponType.BOW,    damage=22)

    hero.equip_weapon(sword)
    hero.equip_weapon(dagger)
    hero.equip_weapon(bow)
    print(f"Total damage potential: {hero.total_damage_potential()}")  # 70

    # ── Learn skills (set — duplicates silently ignored) ──────────────────────
    hero.learn_skill("Shield Bash")
    hero.learn_skill("Battle Cry")
    hero.learn_skill("Shield Bash")    # duplicate → returns False
    print(f"Skills learned: {hero.skills}")

    # ── Pick up items (defaultdict groups by ItemType) ────────────────────────
    hero.pick_up_item(Item("Health Potion", ItemType.POTION, value=50))
    hero.pick_up_item(Item("Mana Potion",   ItemType.POTION, value=40))
    hero.pick_up_item(Item("Iron Shield",   ItemType.ARMOR,  value=120))
    grouped = {k: [i.name for i in v] for k, v in hero.items_by_type().items()}
    print(f"Items by type: {grouped}")

    # ── Combat simulation ─────────────────────────────────────────────────────
    hero.take_damage(35)
    # print(hero)
    hero.take_damage(20)
    # print(hero)
    hero.heal(25)
    # print(hero)

    # ── Record kills (Counter) ────────────────────────────────────────────────
    for _ in range(5): hero.record_kill("Goblin")
    for _ in range(3): hero.record_kill("Orc")
    hero.record_kill("Dragon")
    print(f"Top kills: {hero.top_kills()}")

    # ── Upgrade stat (dict) ───────────────────────────────────────────────────
    hero.upgrade_stat("strength", 5)
    print(f"Strength after upgrade: {hero.stats['strength']}")   # 15

    # ── Rolling combat log (deque, last 10 entries) ───────────────────────────
    print("\n=== Combat Log (last 10 entries) ===")
    for entry in hero.combat_log:
        print(" ", entry)


if __name__ == "__main__":
    main()
