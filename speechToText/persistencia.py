from speechToText.models import Dicho, File


def insert_dicho_row(author):
    last_id = search_last_dicho_pk()
    return Dicho.objects.create(file_id=last_id, author=author)


def insert_file_row(attached_file, id_file, isVideo):
    try:
        for chunk in attached_file.chunks():
            attached_file.write(chunk)
            if isVideo:
                print("Creando registro en base de datos")
                return File.objects.create(id_file=id_file, file_attached=chunk)
            else:
                print("Creando registro en base de datos")
                return File.objects.create(id_file=id_file, file_attached=chunk, file_type=attached_file.content_type)
    except Exception as e:
        print(e)


def update_file_table(update_row, uri):
    try:
        update_row.file_uri = uri
        print("Updeteando tabla FILE")
        update_row.save()
    except Exception as e:
        print(e)
        print("Hubo un problema en el metodo update_file_table()")


def update_dicho_table(update_row, recognized_text):
    try:
        print("Updteando tabla DICHOS")
        update_row.recognized_text = recognized_text
        update_row.save()
    except Exception as e:
        print(e + "Hubo un problema en el metodo update_dicho_table()")


def search_last_dicho_pk():
    try:
        return Dicho.objects.latest('file_id').pk + 1
    except Exception as e:
        return 1
