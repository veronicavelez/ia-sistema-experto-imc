import tkinter as tk
from clips import Environment

env = Environment()

env.build("(deftemplate persona (slot imc) (slot genero))")

env.build("""
(defrule clasificacion-bajo-peso
  (persona (imc ?v) (genero ?g))
  (test (< ?v 18.5))
  =>
  (assert (clasificacion bajo-peso)))
""")
env.build("""
(defrule clasificacion-peso-normal
  (persona (imc ?v) (genero ?g))
  (test (and (>= ?v 18.5) (< ?v 25)))
  =>
  (assert (clasificacion peso-normal)))
""")
env.build("""
(defrule clasificacion-sobrepeso
  (persona (imc ?v) (genero ?g))
  (test (and (>= ?v 25) (< ?v 30)))
  =>
  (assert (clasificacion sobrepeso)))
""")
env.build("""
(defrule clasificacion-obesidad
  (persona (imc ?v) (genero ?g))
  (test (>= ?v 30))
  =>
  (assert (clasificacion obesidad)))
""")

env.build("""
(defrule recomendacion-bajo-peso
  (persona (imc ?v) (genero ?g))
  (test (< ?v 18.5))
  =>
  (assert (recomendacion "Se recomienda aumentar la ingesta calórica con alimentos ricos en nutrientes y realizar ejercicios de fuerza.")))
""")
env.build("""
(defrule recomendacion-peso-normal
  (persona (imc ?v) (genero ?g))
  (test (and (>= ?v 18.5) (< ?v 25)))
  =>
  (assert (recomendacion "Mantén tu estilo de vida saludable con alimentación equilibrada y actividad física regular.")))
""")
env.build("""
(defrule recomendacion-sobrepeso
  (persona (imc ?v) (genero ?g))
  (test (and (>= ?v 25) (< ?v 30)))
  =>
  (assert (recomendacion "Reduce la ingesta de azúcares y grasas. Incrementa la actividad física cardiovascular.")))
""")
env.build("""
(defrule recomendacion-obesidad
  (persona (imc ?v) (genero ?g))
  (test (>= ?v 30))
  =>
  (assert (recomendacion "Consulta con un especialista. Adopta un plan estructurado de alimentación y ejercicio.")))
""")

env.build("""
(defrule recomendacion-bajo-peso-femenino
  (persona (imc ?v) (genero femenino))
  (test (< ?v 18.5))
  =>
  (assert (recomendacion-genero "Como mujer, es importante cuidar también tu salud ósea. Considera evaluación nutricional especializada.")))
""")

def calcular():
    try:
        peso = float(entry_peso.get())
        estatura = float(entry_estatura.get())
        genero = genero_var.get()

        if peso <= 0 or estatura <= 0:
            raise ValueError("Peso y estatura deben ser mayores a cero.")

        imc = peso / (estatura ** 2)

        env.reset()
        env.assert_string(f'(persona (imc {imc}) (genero {genero}))')
        env.run()

        clasificacion = "No clasificado"
        recomendacion = ""
        adicional = ""

        for fact in env.facts():
            if fact.template.name == "clasificacion":
                clasificacion = str(fact).split()[-1].replace(")", "").replace("-", " ").capitalize()
            if fact.template.name == "recomendacion":
                recomendacion = fact[0].replace('"', '')
            if fact.template.name == "recomendacion-genero":
                adicional = fact[0].replace('"', '')

        resultado = f"IMC: {imc:.2f}\nClasificación: {clasificacion}\n\nRecomendación:\n{recomendacion}"
        if adicional:
            resultado += f"\n\n{adicional}"

        lbl_resultado.config(text=resultado, fg="blue")

    except Exception as e:
        lbl_resultado.config(text=f"Error: {str(e)}", fg="red")

ventana = tk.Tk()
ventana.title("Sistema Experto IMC con Recomendaciones - POLI")
ventana.geometry("540x500")
ventana.resizable(False, False)

tk.Label(ventana, text="Sistema Experto: Clasificación del IMC", font=("Helvetica", 14, "bold")).pack(pady=10)

frame = tk.Frame(ventana)
frame.pack(pady=10)

tk.Label(frame, text="Peso (kg):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_peso = tk.Entry(frame)
entry_peso.grid(row=0, column=1)

tk.Label(frame, text="Estatura (m):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_estatura = tk.Entry(frame)
entry_estatura.grid(row=1, column=1)

tk.Label(frame, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
genero_var = tk.StringVar(value="femenino")
tk.OptionMenu(frame, genero_var, "femenino", "masculino").grid(row=2, column=1)

tk.Button(ventana, text="Calcular IMC", command=calcular).pack(pady=10)

lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), wraplength=500, justify="left")
lbl_resultado.pack(pady=10)

tk.Label(ventana, text="Integrantes: Isabel Medina, Laura Murillo, Veronica Velez L", font=("Arial", 9, "italic")).pack(side="bottom", pady=10)

ventana.mainloop()
