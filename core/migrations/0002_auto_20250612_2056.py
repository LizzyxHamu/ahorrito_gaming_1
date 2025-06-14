# core/migrations/0002_...py (el nombre puede variar)

from django.db import migrations

def poblar_datos(apps, schema_editor):
    """
    Función para poblar la base de datos con categorías y productos iniciales.
    """
    # Obtenemos los modelos de la app 'core' para esta migración
    Categoria = apps.get_model('core', 'Categoria')
    Producto = apps.get_model('core', 'Producto')

    # --- CREACIÓN DE CATEGORÍAS ---
    # Usamos get_or_create para no crear duplicados si ya existen
    cat_pc, _ = Categoria.objects.get_or_create(nombre='Juegos de PC')
    cat_ps5, _ = Categoria.objects.get_or_create(nombre='Juegos de PlayStation')
    cat_xbox, _ = Categoria.objects.get_or_create(nombre='Juegos de Xbox')
    cat_switch, _ = Categoria.objects.get_or_create(nombre='Juegos de Nintendo')
    cat_tcg, _ = Categoria.objects.get_or_create(nombre='Cartas TCG')

    # --- CREACIÓN DE PRODUCTOS ---
    # Lista de diccionarios, cada diccionario es un producto
    productos_a_crear = [
        {
            "nombre": "Cyberpunk 2077",
            "descripcion": "Un RPG de acción y aventura de mundo abierto ambientado en Night City.",
            "precio": 13790,
            "stock": 25,
            "categoria": cat_pc
        },
        {
            "nombre": "Elden Ring",
            "descripcion": "Un vasto mundo de fantasía oscura creado por Hidetaka Miyazaki y George R. R. Martin.",
            "precio": 24990,
            "stock": 15,
            "categoria": cat_pc
        },
        {
            "nombre": "Red Dead Redemption 2",
            "descripcion": "La épica historia de Arthur Morgan en el corazón de América en los albores de la era moderna.",
            "precio": 9190,
            "stock": 30,
            "categoria": cat_ps5
        },
        {
            "nombre": "Hogwarts Legacy",
            "descripcion": "Vive la vida como un estudiante en el Colegio Hogwarts de Magia y Hechicería en el siglo XIX.",
            "precio": 39990,
            "stock": 20,
            "categoria": cat_ps5
        },
        {
            "nombre": "Starfield",
            "descripcion": "El primer universo nuevo en más de 25 años de Bethesda Game Studios.",
            "precio": 54990,
            "stock": 10,
            "categoria": cat_xbox
        },
        {
            "nombre": "Zelda: Tears of the Kingdom",
            "descripcion": "Una aventura épica a través de la tierra y los cielos de Hyrule te espera.",
            "precio": 49990,
            "stock": 18,
            "categoria": cat_switch
        },
    ]

    # Recorremos la lista y creamos cada producto
    for datos_producto in productos_a_crear:
        Producto.objects.create(
            nombre=datos_producto["nombre"],
            descripcion=datos_producto["descripcion"],
            precio=datos_producto["precio"],
            stock=datos_producto["stock"],
            categoria=datos_producto["categoria"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'), # Depende de la migración que creó las tablas
    ]

    operations = [
        # Aquí le decimos a Django que ejecute nuestra función
        migrations.RunPython(poblar_datos),
    ]