import tkinter as tk
from clips import Environment

# Crear entorno CLIPS
env = Environment()

# Definir template y reglas
env.build("(deftemplate persona (slot imc))")

env.build("""
(defrule bajo-peso
  (persona (imc ?v))
  (test (< ?v 18.5))
  =>
  (assert (clasificacion bajo-peso)))
""")
env.build("""
(defrule peso-normal
  (persona (imc ?v))
  (test (and (>= ?v 18.5) (< ?v 25)))
  =>
  (assert (clasificacion peso-normal)))
""")
env.build("""
(defrule sobrepeso
  (persona (imc ?v))
  (test (and (>= ?v 25) (< ?v 30)))
  =>
  (assert (clasificacion sobrepeso)))
""")
env.build("""
(defrule obesidad
  (persona (imc ?v))
  (test (>= ?v 30))
  =>
  (assert (clasificacion obesidad)))
""")

# Lógica para cálculo del IMC
def calcular_imc():
    try:
        peso = float(entry_peso.get())
        estatura = float(entry_estatura.get())
        if estatura <= 0:
            raise ValueError("La estatura debe ser mayor a cero.")
        imc = peso / (estatura ** 2)

        env.reset()
        env.assert_string(f"(persona (imc {imc}))")
        env.run()

        clasificacion = "No clasificado"
        for fact in env.facts():
            if fact.template.name == "clasificacion":
                clasificacion = fact.slots[0].replace("-", " ").capitalize()

        resultado = f"IMC: {imc:.2f} → Clasificación: {clasificacion}"
        lbl_resultado.config(text=resultado, fg="blue")

    except ValueError as e:
        lbl_resultado.config(text=f"Error: {str(e)}", fg="red")

# Interfaz de usuario
ventana = tk.Tk()
ventana.title("Sistema Experto IMC - CLIPSPY - POLI")
ventana.geometry("500x400")
ventana.resizable(False, False)

tk.Label(ventana, text="Sistema Experto: Clasificación del IMC POLI", font=("Helvetica", 14, "bold")).pack(pady=10)
tk.Label(ventana, text="Ingrese sus datos para conocer su clasificación según el IMC.").pack()

frame_inputs = tk.Frame(ventana)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Peso (kg):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_peso = tk.Entry(frame_inputs)
entry_peso.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Estatura (m):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_estatura = tk.Entry(frame_inputs)
entry_estatura.grid(row=1, column=1, padx=5, pady=5)

tk.Button(ventana, text="Calcular IMC", command=calcular_imc).pack(pady=10)

lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), fg="blue")
lbl_resultado.pack(pady=10)

frame_footer = tk.Frame(ventana)
frame_footer.pack(side="bottom", pady=15)
tk.Label(frame_footer, text="Integrantes: Isabel Medina, Laura Murillo, Veronica Velez L", font=("Arial", 9, "italic")).pack()

ventana.mainloop()
