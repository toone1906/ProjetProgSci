import ast
import glob
import os

def extract_docstrings_to_markdown(output_file="Documentation_Projet.md"):

    files = sorted(glob.glob("*.py"))

    current_script = os.path.basename(__file__)
    if current_script in files:
        files.remove(current_script)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# Documentation du Projet\n\n")
        out.write(f"Généré automatiquement pour : {', '.join(files)}\n\n---\n\n")

        for file_path in files:
            print(f"Extraction de {file_path}...")
            
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            
            try:
                tree = ast.parse(source)
            except SyntaxError:
                print(f"Erreur de syntaxe dans {file_path}, ignoré.")
                continue

            out.write(f"## Fichier : `{file_path}`\n\n")

            module_doc = ast.get_docstring(tree)
            if module_doc:
                out.write(f"**Description du module :**\n\n>{module_doc.replace(chr(10), chr(10)+'> ')}\n\n")
            
            functions_found = False
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    functions_found = True
                    name = node.name
                    type_obj = "Fonction" if isinstance(node, ast.FunctionDef) else "Classe"
                    
                    
                    doc = ast.get_docstring(node)
                    
                    out.write(f"### {type_obj} : `{name}`\n")
                    if doc:
                        
                        formatted_doc = doc.replace('\n', '\n> ')
                        out.write(f"> {formatted_doc}\n\n")
                    else:
                        out.write("> *Pas de documentation.*\n\n")
            
            if not functions_found:
                out.write("*Aucune fonction ou classe détectée.*\n\n")
            
            out.write("---\n\n")

    print(f"\nsuccès ! La documentation a été sauvegardée dans : {output_file}")

if __name__ == "__main__":
    extract_docstrings_to_markdown()