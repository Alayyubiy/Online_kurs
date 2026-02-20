import os

# Natija yoziladigan fayl
output_file = "hamma_kodlar.txt"

with open(output_file, "w", encoding="utf-8") as f_out:
    for root, dirs, files in os.walk("."):
        for file in files:
            # Skriptning o'zini va natija faylini qo'shib yubormaslik uchun
            if file.endswith((".py", ".js", ".html", ".css", ".cpp", ".java")) and file != output_file:
                f_out.write(f"\n\n--- FAYL NOMI: {file} ---\n")
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f_in:
                        f_out.write(f_in.read())
                except:
                    f_out.write("[Xatolik: Faylni o'qib bo'lmadi]")

print(f"Tayyor! Hamma kodlar '{output_file}' fayliga yig'ildi.")