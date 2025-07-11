from django.db import migrations
from django.utils.text import slugify


PRODUCTOS_DATA = [
    # Juegos de PlayStation 5
    {'nombre': 'Stellar Blade', 'precio': 64990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Aventura de acción post-apocalíptica con combate trepidante.'},
    {'nombre': 'Rise of the Ronin', 'precio': 69990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Ambientado en el Japón del siglo XIX, este juego de acción ofrece combates intensos y una narrativa profunda.'},
    {'nombre': 'Final Fantasy VII Rebirth', 'precio': 64990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'La segunda entrega del proyecto remake de FINAL FANTASY VII.'},
    {'nombre': 'Helldivers 2', 'precio': 39990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Shooter cooperativo en tercera persona donde luchas por la libertad en una galaxia hostil.'},
    {'nombre': "Elden Ring Shadow of the Erdtree Collector's Edition", 'precio': 249990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Edición coleccionista de la expansión de Elden Ring, incluye figura y libro de arte.'},
    {'nombre': 'Elden Ring Shadow of the Erdtree Edition', 'precio': 69990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Incluye el juego base Elden Ring y la expansión Shadow of the Erdtree.'},
    {'nombre': 'Shin Megami Tensei V: Vengeance', 'precio': 59990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'La versión definitiva de Shin Megami Tensei V.'},
    {'nombre': 'TopSpin 2K25', 'precio': 59990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'El regreso de la aclamada saga de tenis.'},
    {'nombre': 'Sand Land', 'precio': 56990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Basado en la obra de Akira Toriyama.'},
    {'nombre': 'Eiyuden Chronicle: Hundred Heroes', 'precio': 49990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Un JRPG moderno con la estética y el espíritu de los clásicos del género.'},
    {'nombre': "Dragon's Dogma 2", 'precio': 64990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Un RPG de acción para un jugador que te permite elegir tu propia experiencia.'},
    {'nombre': 'One Piece Odyssey', 'precio': 42990, 'categoria': 'Juegos PlayStation 5', 'descripcion': 'Aventura RPG protagonizada por Luffy y la tripulación del Sombrero de Paja.'},
    {'nombre': 'PSVR2 Horizon Call Of The Mountain Bundle', 'precio': 624990, 'categoria': 'Accesorios PlayStation 5', 'descripcion': 'Pack de realidad virtual que incluye el nuevo visor PSVR2 y el juego Horizon Call of the Mountain.'},
    {'nombre': 'Princess Peach: Showtime!', 'precio': 54990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'Peach se convierte en la estrella del espectáculo.'},
    {'nombre': 'Mario vs. Donkey Kong', 'precio': 49990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'El clásico juego de puzles y plataformas regresa con gráficos renovados.'},
    {'nombre': 'The Legend of Zelda: Tears of the Kingdom', 'precio': 59990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'Una aventura épica a través de la tierra y los cielos de Hyrule te espera.'},
    {'nombre': 'Super Mario Bros. Wonder', 'precio': 54990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'La nueva evolución de los juegos de Mario en 2D.'},
    {'nombre': 'Endless Ocean Luminous', 'precio': 49990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'Sumérgete en un misterioso mundo submarino que cambia con cada inmersión.'},
    {'nombre': 'Another Code: Recollection', 'precio': 54990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'Resuelve los misterios del pasado de Ashley Mizuki Robins en esta colección remasterizada.'},
    {'nombre': 'Super Bomberman R 2', 'precio': 49990, 'categoria': 'Juegos Nintendo Switch', 'descripcion': 'Clásico multijugador con nuevas funciones.'},
    {'nombre': 'WWE 2K24', 'precio': 59990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Revive los momentos más grandes de WrestleMania.'},
    {'nombre': 'Persona 3 Reload', 'precio': 64990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Sumérgete en la Hora Oscura y despierta los poderes de tu corazón.'},
    {'nombre': 'Like a Dragon: Infinite Wealth', 'precio': 64990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Dos héroes extraordinarios unidos por el destino.'},
    {'nombre': 'Resident Evil 4', 'precio': 44990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'La supervivencia es solo el comienzo en esta reinvención del clásico de terror.'},
    {'nombre': 'Mortal Kombat 1', 'precio': 49990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Descubre un nuevo universo de Mortal Kombat renacido.'},
    {'nombre': "Jojo's Bizarre Adventure: All-Star Battle R", 'precio': 181990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Juego de lucha basado en el famoso anime JoJo\'s Bizarre Adventure.'},
    {'nombre': 'Demon Slayer: The Hinokami Chronicles', 'precio': 41990, 'categoria': 'Juegos PlayStation 4', 'descripcion': 'Acción intensa en este título basado en la popular serie Demon Slayer.'},
    {'nombre': 'The Callisto Protocol', 'precio': 39990, 'categoria': 'Juegos de PC', 'descripcion': 'Terror espacial con gráficos de última generación.'},
    {'nombre': 'Payday 3', 'precio': 39990, 'categoria': 'Juegos de PC', 'descripcion': 'Juego cooperativo de acción y estrategia donde planeas y ejecutas robos.'},
    {'nombre': 'Star Wars Outlaws', 'precio': 69990, 'categoria': 'Juegos de PC', 'descripcion': 'Explora el universo Star Wars en este juego de mundo abierto.'},
    {'nombre': 'Consola Nintendo Switch OLED The Legend of Zelda: Tears of the Kingdom', 'precio': 349990, 'categoria': 'Consolas Nintendo Switch', 'descripcion': 'Edición especial de la consola con motivos del aclamado juego.'},
    {'nombre': 'Consola Nintendo Switch 1.1 Neon', 'precio': 299990, 'categoria': 'Consolas Nintendo Switch', 'descripcion': 'La versátil consola de Nintendo en su versión estándar con Joy-Cons color neón.'},
    {'nombre': 'Fuente de Poder para Consola Wii Multivoltaje', 'precio': 12990, 'categoria': 'Accesorios Wii', 'descripcion': 'Fuente de poder de reemplazo para la consola Nintendo Wii.'},
    {'nombre': 'Carta Pokémon TCG: Charizard ex - SV4.5 Paldean Fates', 'precio': 39990, 'categoria': 'Cartas TCG', 'descripcion': 'Carta individual de alta rareza del popular juego de cartas coleccionables Pokémon.'},
    {'nombre': 'Disney Lorcana: Booster Box The First Chapter', 'precio': 149990, 'categoria': 'Cartas TCG', 'descripcion': 'Caja sellada con 24 sobres de la primera edición del juego de cartas Disney Lorcana.'},
    {'nombre': 'Star Wars: Unlimited - Caja de Sobres', 'precio': 129990, 'categoria': 'Cartas TCG', 'descripcion': 'Caja sellada con 24 sobres del nuevo juego de cartas coleccionables de Star Wars.'},
]

def poblar_datos(apps, schema_editor):
    Categoria = apps.get_model('core', 'Categoria')
    Producto = apps.get_model('core', 'Producto')

    # Diccionario para guardar las categorías ya creadas y evitar consultas repetidas
    categorias_creadas = {}

    for item in PRODUCTOS_DATA:
        nombre_cat = item['categoria']
        # Si no hemos procesado esta categoría antes, la creamos
        if nombre_cat not in categorias_creadas:
            slug = slugify(nombre_cat)
            # Usamos get_or_create con 'defaults' para crear la categoría y su slug
            # de forma atómica y segura. Esto soluciona el IntegrityError.
            cat_obj, created = Categoria.objects.get_or_create(
                nombre=nombre_cat,
                defaults={'slug': slug}
            )
            categorias_creadas[nombre_cat] = cat_obj

    # Ahora creamos los productos con la certeza de que las categorías ya existen
    for item in PRODUCTOS_DATA:
        if not all(k in item for k in ['nombre', 'categoria', 'precio']):
            continue
        
        # Generamos los tags automáticamente para potenciar la búsqueda
        tags_set = set(item.get('nombre', '').lower().split() + item.get('categoria', '').lower().split())
        stop_words = {'de', 'la', 'el', 'y', 'con', 'para', 'juegos', 'edición', 'a', 'un'}
        tags_finales = ", ".join(list(tags_set - stop_words))
        
        categoria_obj = categorias_creadas[item['categoria']]
        
        # Usamos update_or_create para que la migración sea segura de ejecutar múltiples veces
        Producto.objects.update_or_create(
            nombre=item['nombre'],
            defaults={
                'precio': item['precio'],
                'descripcion': item.get('descripcion', ''),
                'categoria': categoria_obj,
                'tags': tags_finales,
                'stock': 20,
                'activo': True,
            }
        )

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(poblar_datos),
    ]