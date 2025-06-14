# Suavizado de mallas poligonales utilizando el algoritmo **Rain Filter**

## Introducción

El **Rain Filter** [**Rain Filter**](https://www.dropbox.com/scl/fi/tizbmmv92zbhrmsgulee6/Rain-Filter.pdf?rlkey=rl3la5kkztk7pr1q5nmgd7rbz&dl=0) propone un enfoque de suavizado en el que **el ruido aleatorio actúa como filtro emergente**. A diferencia de métodos deterministas —por ejemplo, un filtro Laplaciano clásico—, aquí se lanzan *gotas* (perturbaciones estocásticas) sobre la malla y **solo se aceptan si contrarrestan la curvatura local**: las crestas se erosionan y los valles se rellenan. El resultado final es un suavizado global, pero lo interesante del método reside en **los pasos intermedios y su aleatoriedad controlada**.

---

## Descripción:

1. **Medida local de relieve**

   Para un vértice $v$ con vecinos $\{v_i\}$:

   $\mathbf{c}=\frac{1}{N}\sum_i v_i, \qquad \mathbf{d}=v-\mathbf{c}$

   El escalar de curvatura proyectada es:

   $\kappa = \mathbf{d}\cdot\mathbf{n}$

   donde $\mathbf{n}$ es la **normal local**.

2. **Generación de la gota**

   Se elige un vector ruido unitario $\mathbf{r}\in[-1,1]^3$ (distribución uniforme).

3. **Condición de antifase**

   La gota se aplica **solo si**:

   $\kappa\,(\mathbf{r}\cdot\mathbf{n}) < 0$

   de modo que siempre tiende a *aplanar* la superficie.

4. **Desplazamiento**

   $\Delta\mathbf{v}=\alpha\,|\kappa|\,\mathbf{r}$

   donde $\alpha$ es la intensidad base, amplificada exponencialmente por iteración:

   $\alpha_i = \alpha_0\,\text{growth}^i$

   > **Nota:** Esta amplificación exponencial **no forma parte del concepto original del Rain Filter**, pero resulta necesaria en aplicaciones sobre mallas tridimensionales, donde muchas regiones presentan curvaturas pequeñas. Sin esta intensificación progresiva, el filtro no tendría efecto apreciable en esas áreas. En contexto DSP, un mecanismo similar podría aplicarse, pero debe manejarse con cuidado: **una ganancia exponencial puede provocar artefactos o explosiones sónicas**.

5. **Iteración**

   El proceso se repite varias pasadas; el suavizado emerge de la acumulación.

---

## Implementación en Blender (**Pure Rain Smooth 1.2.1**)

* **Dirección local:** se usa la normal individual de cada vértice.
* **Pasadas tangenciales (opcionales):** dos direcciones ortogonales locales para un efecto más isotrópico.
* **Amplificación exponencial:** controla la velocidad de convergencia (`growth ∈ [1 – 1.3]`).
* **Clamp de seguridad:** limita cada desplazamiento a 0.05 BU, evitando explosiones geométricas.

> *Existen métodos más eficientes y teóricamente robustos para suavizar mallas (p. ej. Laplaciano discreto completo o Taubin smooth). Aquí se prioriza la **fidelidad conceptual** al modelo Rain Filter sobre la optimización, a modo de prueba de concepto.*

---

## Discusión

* Los primeros pasos apenas alteran la malla; al acumular iteraciones y con la amplificación exponencial, el relieve converge rápidamente hacia la planitud.
* La **aleatoriedad** de las gotas crea microvariaciones que no produce un filtro determinista, proporcionando un aspecto más *natural*.
* Posibles mejoras productivas:

  1. Sustituir la curvatura proyectada por un Laplaciano completo.
  2. Implementar el proceso como **modificador no destructivo**.
  3. Controlar la lluvia mediante **mapas de peso** o texturas.

---

## Próximos pasos

1. **Implementación en audio:** se explora un prototipo en *Pure Data* donde el ruido se inyecta como gotas antifase condicionadas por la forma de la señal.
2. **Mejoras en Blender:**

   * Curvaturas más precisas, sin comprometer la filosofía.
   * Conversión a modificador procedural animable.
   * Soporte de mapas de peso para modular espacialmente la lluvia.

Estas direcciones permitirán que el Rain Filter evolucione de prueba algorítmica a herramienta expresiva tanto en gráficos como en sonido.

---

## Conclusiones

El **Rain Filter** demuestra que un filtro puede surgir del **ruido mismo cuando se condiciona por la forma**. El addon **Pure Rain Smooth** implementa fielmente este principio para mallas poligonales:

* Sin convoluciones explícitas,
* Sin kernels fijos,
* Únicamente ruido antifase y curvatura local.

Esto abre la puerta a experimentos análogos en audio DSP o texturas procedurales, donde la dinámica emergente y la fase relativa del ruido podrían desempeñar el mismo papel.

---

## Referencias breves

* Rodríguez, D. (2025). *Rain Filter* (concepto original).
* Taubin, G. (1995). “A signal processing approach to fair surface design.” *SIGGRAPH*.
* **El Mar**, experiencia observacional que inspiró la metáfora de la lluvia calmando las olas.
