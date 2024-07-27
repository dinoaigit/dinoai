import os
from trefle_api import (get_kingdoms, get_subkingdoms, get_divisions,
                        get_classes, get_orders, get_families,
                        get_genuses, get_species)


def create_folder_structure():
    kingdoms = get_kingdoms()

    for kingdom in kingdoms:
        kingdom_name = kingdom['name'].replace('/', '_')
        kingdom_id = kingdom['id']
        os.makedirs(kingdom_name, exist_ok=True)

        subkingdoms = get_subkingdoms(kingdom_id)

        for subkingdom in subkingdoms:
            subkingdom_name = subkingdom['name'].replace('/', '_')
            subkingdom_id = subkingdom['id']
            os.makedirs(os.path.join(kingdom_name, subkingdom_name), exist_ok=True)

            divisions = get_divisions(subkingdom_id)

            for division in divisions:
                division_name = division['name'].replace('/', '_')
                division_id = division['id']
                os.makedirs(os.path.join(kingdom_name, subkingdom_name, division_name), exist_ok=True)

                classes = get_classes(division_id)

                for cl in classes:
                    class_name = cl['name'].replace('/', '_')
                    class_id = cl['id']
                    os.makedirs(os.path.join(kingdom_name, subkingdom_name, division_name, class_name), exist_ok=True)

                    orders = get_orders(class_id)

                    for order in orders:
                        order_name = order['name'].replace('/', '_')
                        order_id = order['id']
                        os.makedirs(os.path.join(kingdom_name, subkingdom_name, division_name, class_name, order_name),
                                    exist_ok=True)

                        families = get_families(order_id)

                        for family in families:
                            family_name = family['name'].replace('/', '_')
                            family_id = family['id']
                            os.makedirs(
                                os.path.join(kingdom_name, subkingdom_name, division_name, class_name, order_name,
                                             family_name), exist_ok=True)

                            genuses = get_genuses(family_id)

                            for genus in genuses:
                                genus_name = genus['name'].replace('/', '_')
                                genus_id = genus['id']
                                os.makedirs(
                                    os.path.join(kingdom_name, subkingdom_name, division_name, class_name, order_name,
                                                 family_name, genus_name), exist_ok=True)

                                species = get_species(genus_id)

                                for specie in species:
                                    species_name = specie['name'].replace('/', '_')
                                    os.makedirs(os.path.join(kingdom_name, subkingdom_name, division_name, class_name,
                                                             order_name, family_name, genus_name, species_name),
                                                exist_ok=True)


if __name__ == "__main__":
    create_folder_structure()
