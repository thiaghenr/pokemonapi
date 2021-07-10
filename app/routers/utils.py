from .pokemon_type import get_pokemon_type


def get_pokemon_types(pokemon_association, db):
    return [get_pokemon_type(tp_id.pokemontype_id, db)
                        for tp_id in pokemon_association]