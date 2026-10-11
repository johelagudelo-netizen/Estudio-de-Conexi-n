import matplotlib.pyplot as plt
import numpy as np

# Generar datos de ejemplo
x = np.linspace(0.1, 1e4, 500)  # Valores de x entre 0.01 y 10000
y = 2 * x                        # y es el doble de x

# Crear la figura y los ejes
Fig3 = plt.figure(figsize=(10, 12)) 
ax3 = Fig3.add_subplot(111)

# Graficar los datos
ax3.plot(x, y, label='y = 2 * x')

# Configurar los ejes y la gráfica utilizando plt
plt.xlabel('Corriente (A)')
plt.ylabel('Tiempo(s)')
plt.grid(True, which='both')
plt.xscale('log')
plt.yscale('log')
plt.title('Ejemplo de Gráfica Logarítmica con y = 2 * x')

# Definir los límites de los ejes utilizando ax3
ax3.set_xlim(1, 1e4)
ax3.set_ylim(0.01, 1e2)

# Mostrar la leyenda
plt.legend()

# Mostrar la gráfica
plt.show()
