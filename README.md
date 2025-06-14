# PureRainSmooth
Mesh smoothing algorithm 
Suavizado de mallas poligonales
 utilizando el algoritmoRain Filter
 Introducción
 El Rain Filter propone un enfoque de suavizado en el que el ruido aleatorio actúa como
 filtro emergente. A diferencia de métodos deterministas —por ejemplo, un filtro Laplaciano
 clásico—, aquí se lanzan "gotas" (perturbaciones estocásticas) sobre la malla y sólo se
 aceptan si contrarrestan la curvatura local: las crestas se erosionan y los valles se
 rellenan. El resultado final es un suavizado global, pero lo interesante del método reside en
 los pasos intermedios y su aleatoriedad controlada.
 Descripción matemática mínima
 1. Medida local de relieve
 Para un vértice vv con vecinos {vi}\{v_i\}:
 c=1N∑ivi,d= v−c\mathbf{c} = \frac{1}{N}\sum_i v_i, \quad \mathbf{d}=\,v-\mathbf{c}
 El escalar de curvatura proyectada es
 κ=d⋅n\kappa = \mathbf{d}\cdot\mathbf{n}
 donde n\mathbf{n} es la normal local.
 2. Generación de la gota
 Se elige un vector ruido unitario r∈[−1,1]3\mathbf{r}\in[-1,1]^3 (distribución
 uniforme).
 3. Condición de antifase
 La gota se aplica sólo si
 κ (r⋅n)<0\kappa\,(\mathbf{r}\cdot\mathbf{n}) < 0
 de modo que siempre tiende a "aplanar" la superficie.
 4. Desplazamiento
 Δv=α ∣κ∣ r\Delta\mathbf{v} = \alpha\,|\kappa|\,\mathbf{r}
 donde α\alpha es la intensidad base, amplificada exponencialmente por iteración:
 αi=α0 growthi\alpha_i = \alpha_0\,\mathrm{growth}^i.
 Esta amplificación exponencial no forma parte del concepto original del Rain
 Filter, pero resulta necesaria en aplicaciones sobre mallas tridimensionales, donde
 muchas regiones presentan curvaturas pequeñas. Sin esta intensificación
 progresiva, el filtro no tendría efecto apreciable en esas áreas. En el contexto del
 procesamiento de señales digitales (DSP), un mecanismo similar podría aplicarse,
pero se recomienda precaución: una ganancia exponencial podría derivar en
 artefactos o explosiones sónicas, si no se regula adecuadamente.
 5. Iteración
 El proceso se repite varias pasadas; el suavizado emerge de la acumulación.
 Implementación en Blender (Pure Rain Smooth 1.2.1)
 ● Dirección local: se usa la normal de cada vértice.
 ● Pasadas tangenciales (opcionales): se añaden dos direcciones ortogonales
 locales para un efecto más isotrópico.
 ● Amplificación exponencial: controla la velocidad de convergencia (growth
 ∈[1,1.3]\in[1,1.3]).
 ● Clamp: evita explosiones geométricas limitando cada desplazamiento a 0.05 BU.
 Nota: Existen métodos más eficientes y teóricamente robustos para suavizar
 mallas (p. ej. Laplaciano discreto completo o Taubin smooth). Aquí se prioriza
 la fidelidad conceptual al modelo Rain Filter sobre la optimización, a modo de
 prueba de concepto.
 Discusión
 ● El algoritmo exhibe un comportamiento interesante: los primeros pasos apenas
 alteran la malla; sin embargo, al acumular iteraciones —y con la amplificación— el
 relieve converge rápidamente hacia la planitud.
 ● Laaleatoriedad de las gotas crea microvariaciones que no produce un filtro
 determinista, dando un aspecto más "natural".
 ● Para producción se podría:
 1. Sustituir la curvatura proyectada por un Laplaciano completo.
 2. Implementar el proceso como modificador no destructivo.
 3. Controlar visualmente la lluvia (densidad espacial, mapas de peso).
Próximos pasos
 Aunque Pure Rain Smooth ya es funcional como addon, hay dos líneas de desarrollo
 claras:
 1. Implementación en audio: El Rain Filter fue concebido como una idea para
 procesamiento de señales digitales (DSP), particularmente audio. Ya se está
 trabajando en un prototipo dentro de Pure Data, donde el ruido se inyecta como
 gotas antifase condicionadas por la forma de la señal.
 2. Mejora e integración en Blender: Se plantea llevar el addon a otro nivel mediante:
 ○ Uso de curvaturas más precisas (por ejemplo, Laplaciana discreta) solo si no
 compromete el concepto.
 ○ Conversión del sistema en un modificador no destructivo, con posibilidad
 de animar los parámetros (iteraciones, intensidad, densidad, etc.).
 ○ Incorporación de mapas de peso o textura para modular espacialmente la
 lluvia.
 Estas direcciones permitirán que el Rain Filter trascienda su papel como curiosidad
 algorítmica y se convierta en una herramienta expresiva tanto en gráficos como en sonido.
 Conclusiones
 El Rain Filter demuestra que un filtro puede surgir del ruido mismo cuando se condiciona
 por la forma. El addon Pure Rain Smooth implementa fielmente este principio para mallas
 poligonales:
 ● Sin convoluciones explícitas,
 ● Sin kernels fijos,
 ● Sólo ruido antifase y curvatura local.
 Esto abre la puerta a experimentos análogos en audio DSP o texturas procedurales, donde
 la dinámica emergente y la fase relativa del ruido podrían desempeñar el mismo papel.
Referencias breves
 ● Rodríguez, D. (2025). Rain Filter (concepto original).
 ● Taubin, G. (1995). “A signal processing approach to fair surface design.”
 SIGGRAPH.
 ● El Mar, que fue mi principal referencia y fuente de inspiración.
