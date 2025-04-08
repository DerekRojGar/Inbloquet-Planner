import pandas as pd
from io import StringIO

# ----- Datos de texto (simulando los CSV) -----

txt_estudiantes = """matricula	nombre	sexo	fecha_inscripcion	id_grado	id_nivel_educativo	estado_matricula
1	santiago arguello garita	h	16/07/2019	2	2	inactivo
2	leonardo guevara yanez	h	15/07/2019	2	2	inactivo
3	patricio tsakiris parra urban	h	16/07/2019	2	2	inactivo
4	emmanuel juarez martinez	h	22/07/2019	2	2	inactivo
5	emiliano gonzalez franco	h	22/07/2019	2	2	inactivo
6	hector manuel salazar melendez	h	25/07/2019	2	2	inactivo
7	aldo	h	25/07/2019	2	2	inactivo
8	iam	h	25/07/2019	2	2	inactivo
9	ximena moralez gonzalez	m	29/07/2019	2	2	inactivo
10	ximena gonzalez franco	m	05/08/2019	2	2	inactivo
11	joaquin rivera grados	h	12/08/2019	1	2	inactivo
12	diego hernandez llaca	h	31/10/2019	1	2	inactivo
13	jean	h	18/11/2019	1	2	inactivo
14	matias	h	17/01/2020	1	2	inactivo
15	evan	h	01/02/2020	1	2	inactivo
16	esteban garcia ramirez	h	15/02/2020	1	2	inactivo
17	valeria vargas garcia	m	15/02/2020	1	2	inactivo
18	rodrigo velazquez manning	h	13/02/2020	1	2	inactivo
19	elias velazquez manning	h	13/02/2020	1	2	inactivo
20	ian santiago lobato diaz	h	29/02/2020	1	2	inactivo
21	naomi america aguirre lopez	m	29/02/2020	1	2	inactivo
22	renata angeles miron	m	29/02/2020	1	2	inactivo
23	jonathan	h	06/03/2020	1	2	inactivo
24	paula vargas salgado	m	09/03/2020	1	2	inactivo
25	emilia vargas salgado	m	09/03/2020	1	2	inactivo
26	pablo andrade salomon	h	17/11/2020	1	2	inactivo
27	mateo andrade salomon	h	17/11/2020	1	2	inactivo
28	derek matias zapata landa	h	19/11/2020	1	2	inactivo
29	iker zapata landa	h	01/01/1980	1	1	inactivo
30	nico	h	01/01/1980	1	2	inactivo
31	viktoria	m	01/01/1980	1	1	inactivo
32	santiago ocampo zamora	h	01/01/1980	1	2	inactivo
33	raul eduardo rojas ramirez	h	01/01/1980	1	2	inactivo
34	axel	h	01/01/1980	1	2	inactivo
35	maximiliano hernandez lopez	h	29/05/2021	1	2	inactivo
36	emma gagnon	m	30/06/2021	2	2	inactivo
37	santiago gagnon	h	30/06/2021	2	2	inactivo
38	hector ezequiel jimenez arriaga	h	02/07/2021	2	2	inactivo
39	alexa montanez fernandez	m	17/07/2021	2	2	inactivo
40	christopher montanez fernandez	h	17/07/2021	2	2	inactivo
41	alexia parrilla reyes	m	20/07/2021	2	2	inactivo
42	alexander parrilla reyes	h	20/07/2021	2	2	inactivo
43	alessio caltagirone valencia	h	27/07/2021	1	2	inactivo
44	diego michel verhaar carrasco	h	02/08/2021	2	2	inactivo
45	melisa	m	02/08/2021	2	2	inactivo
46	alexander	h	01/01/1980	2	2	inactivo
47	sebastian barredo peregrina	h	26/08/2021	1	2	activo
48	alec lopezsainz arnal	h	08/09/2021	1	2	inactivo
49	jose manuel leal dominguez	h	08/09/2021	1	1	inactivo
50	mateo sanchez blanco	h	01/01/1980	1	1	inactivo
51	bruno saldivar michel	h	01/01/1980	1	2	inactivo
52	emilio castro bernardi	h	29/03/2022	1	2	inactivo
53	oscar dario martinez miranda campero	h	16/03/2022	1	2	activo
54	pablo	h	01/01/1980	1	2	inactivo
55	leone arek re garibay	h	29/03/2022	1	1	inactivo
56	fahra saldivar michel	m	21/05/2022	1	2	inactivo
57	mateo corona justo	h	12/05/2022	1	2	inactivo
58	ivan	h	08/06/2022	1	2	inactivo
59	stephan sproll arenaa	h	24/06/2022	1	1	inactivo
60	nobu ryan kano cheng	h	29/06/2022	1	2	inactivo
61	diego garcia cabrera	h	05/07/2022	1	2	inactivo
62	emiliano de la vega cona	h	13/07/2022	1	2	inactivo
63	emilio nocedal diaz	h	18/07/2022	1	2	activo
64	regina nocedal diaz	m	18/07/2022	1	2	activo
65	patrick lee osorio	h	25/07/2022	1	1	inactivo
66	enrique emiliano nanez oliva	h	18/08/2022	1	1	inactivo
67	angel genchi toledo	h	23/09/2022	1	2	inactivo
68	ethan rojas reyes	h	24/09/2022	1	2	inactivo
69	israel briones cano	h	15/11/2022	1	1	inactivo
70	ivannia marmolejo marina	m	24/01/2023	1	1	inactivo
71	sebastian fernandez perez	h	25/01/2023	1	2	inactivo
72	matias emilio luqueno martinez	h	09/02/2023	1	2	inactivo
73	renata garcia	m	24/03/2023	1	2	inactivo
74	iker garces jimenez	h	15/04/2023	1	2	activo
75	matias chiguil jimenez	h	24/04/2023	1	2	inactivo
76	valeria loranca montiel	m	27/05/2023	1	2	inactivo
77	josue santiago hernandez salgado	h	27/05/2023	1	2	inactivo
78	sebastian salinas martinez	h	27/05/2023	1	2	inactivo
79	sofia salinas martinez	m	27/05/2023	1	2	inactivo
80	valentino diaz aldrete	h	01/06/2023	1	1	inactivo
81	emilio cortes bustos	h	07/06/2023	1	2	inactivo
82	matthias woyke alonso	h	11/07/2023	1	2	inactivo
83	santiago morales castaneda	h	11/07/2023	1	2	activo
84	santiago aguero lopez	h	03/08/2023	1	2	inactivo
85	dante sebastian canseco porras	h	08/08/2023	1	2	inactivo
86	alejandro barrios alcazar	h	26/08/2023	1	2	inactivo
87	itzae	h	25/11/2023	1	2	inactivo
88	tamara	m	25/11/2023	1	1	inactivo
89	paulet	m	04/12/2023	1	2	inactivo
90	emiliano moreno tejeda	h	04/11/2023	1	1	inactivo
91	paulo peredo	h	15/02/2024	1	1	inactivo
92	santiago sosa zarate	h	04/12/2023	1	2	inactivo
93	eiza sosa zarate	m	04/12/2023	1	2	inactivo
94	minerva perez moran	m	09/01/2024	1	1	activo
95	sebastian montes de oca cruz y corro	h	27/01/2024	1	2	inactivo
96	daniel forcelledo garcia	h	27/01/2024	1	2	inactivo
97	romina lemus lima	m	07/03/2024	1	2	activo
98	nina nueva	m	01/01/1980	1	1	inactivo
99	julian romero romero	h	29/02/2024	1	1	activo
100	sara lerma tejero	m	07/05/2024	1	2	inactivo
101	elisa lerma tejero	m	07/05/2024	1	2	inactivo
102	daniel ceballos	h	01/01/1980	1	1	inactivo
"""

txt_cursos = """id_curso\tnombre\tid_maestro
1\tClases\t4
2\tVerano\t4
3\tAmbos\t4
"""

txt_paquetes = """id_paquete\tnombre\tcantidad_clases
1\tpaquete sencillo\t8
2\tpaquete completo\t10
"""

txt_grados = """id_grado\tnombre\tid_nivel_educativo
1\tPreescolar\t1
2\tPrimaria\t2
"""

txt_niveles = """id_nivel_educativo\tnombre
1\tpreescolar
2\telemental
3\tambos
"""

txt_estudiantes_cursos = """matricula\tid_curso\tfecha_inscripcion
1\t2\t16/07/2019
2\t2\t15/07/2019
3\t2\t16/07/2019
4\t2\t22/07/2019
5\t2\t22/07/2019
6\t2\t25/07/2019
7\t2\t25/07/2019
8\t2\t25/07/2019
9\t2\t29/07/2019
10\t2\t05/08/2019
11\t1\t12/08/2019
12\t1\t31/10/2019
13\t1\t18/11/2019
14\t1\t17/01/2020
15\t1\t01/02/2020
16\t1\t15/02/2020
17\t1\t15/02/2020
18\t1\t13/02/2020
19\t1\t13/02/2020
20\t1\t29/02/2020
21\t1\t29/02/2020
22\t1\t29/02/2020
23\t1\t06/03/2020
24\t1\t09/03/2020
25\t1\t09/03/2020
26\t1\t17/11/2020
27\t1\t17/11/2020
28\t1\t19/11/2020
29\t1\t01/01/1980
30\t1\t01/01/1980
31\t1\t01/01/1980
32\t1\t01/01/1980
33\t1\t01/01/1980
34\t1\t01/01/1980
35\t1\t29/05/2021
36\t2\t30/06/2021
37\t2\t30/06/2021
38\t2\t02/07/2021
39\t2\t17/07/2021
40\t2\t17/07/2021
41\t2\t20/07/2021
42\t2\t20/07/2021
43\t1\t27/07/2021
44\t2\t02/08/2021
45\t2\t02/08/2021
46\t2\t01/01/1980
47\t1\t26/08/2021
48\t1\t08/09/2021
49\t1\t08/09/2021
50\t1\t01/01/1980
51\t1\t01/01/1980
52\t1\t29/03/2022
53\t1\t16/03/2022
54\t1\t01/01/1980
55\t1\t29/03/2022
56\t1\t21/05/2022
57\t1\t12/05/2022
58\t1\t08/06/2022
59\t1\t24/06/2022
60\t1\t29/06/2022
61\t1\t05/07/2022
62\t1\t13/07/2022
63\t1\t18/07/2022
64\t1\t18/07/2022
65\t1\t25/07/2022
66\t1\t18/08/2022
67\t1\t23/09/2022
68\t1\t24/09/2022
69\t1\t15/11/2022
70\t1\t24/01/2023
71\t1\t25/01/2023
72\t1\t09/02/2023
73\t1\t24/03/2023
74\t1\t15/04/2023
75\t1\t24/04/2023
76\t1\t27/05/2023
77\t1\t27/05/2023
78\t1\t27/05/2023
79\t1\t27/05/2023
80\t1\t01/06/2023
81\t1\t07/06/2023
82\t1\t11/07/2023
83\t1\t11/07/2023
84\t1\t03/08/2023
85\t1\t08/08/2023
86\t1\t26/08/2023
87\t1\t25/11/2023
88\t1\t25/11/2023
89\t1\t04/12/2023
90\t1\t04/11/2023
91\t1\t15/02/2024
92\t1\t04/12/2023
93\t1\t04/12/2023
94\t1\t09/01/2024
95\t1\t27/01/2024
96\t1\t27/01/2024
97\t1\t07/03/2024
98\t1\t01/01/1980
99\t1\t29/02/2024
100\t1\t07/05/2024
101\t1\t07/05/2024
102\t1\t01/01/1980
"""

txt_metodos = """id_metodo\tnombre
1\tEfectivo
2\tDeposito
3\tTransferencia
"""

txt_est_metodos = """matricula\tid_metodo
1\t1
2\t1
3\t1
4\t1
5\t1
6\t1
7\t1
8\t1
9\t1
10\t1
11\t1
12\t1
13\t1
14\t1
15\t1
16\t1
17\t1
18\t1
19\t1
20\t1
21\t1
22\t1
23\t1
24\t1
25\t1
26\t1
27\t1
28\t1
29\t1
30\t1
31\t1
32\t1
33\t1
34\t1
35\t1
36\t1
37\t1
38\t1
39\t1
40\t1
41\t1
42\t1
43\t1
44\t1
45\t1
46\t1
47\t2
48\t1
49\t1
50\t1
51\t1
52\t1
53\t3
54\t1
55\t1
56\t1
57\t1
58\t1
59\t1
60\t1
61\t1
62\t1
63\t3
64\t3
65\t1
66\t1
67\t1
68\t1
69\t1
70\t1
71\t1
72\t1
73\t1
74\t3
75\t1
76\t1
77\t1
78\t1
79\t1
80\t1
81\t1
82\t1
83\t3
84\t1
85\t1
86\t1
87\t3
88\t3
89\t1
90\t1
91\t1
92\t1
93\t1
94\t1
95\t1
96\t1
97\t3
98\t1
99\t3
100\t1
101\t1
102\t1
"""

txt_est_paquetes = """matricula\tid_paquete
1\t1
2\t1
3\t1
4\t1
5\t1
6\t1
7\t1
8\t1
9\t1
10\t1
11\t1
12\t1
13\t1
14\t1
15\t1
16\t1
17\t1
18\t1
19\t1
20\t1
21\t1
22\t1
23\t1
24\t1
25\t1
26\t1
27\t1
28\t1
29\t1
30\t1
31\t1
32\t1
33\t1
34\t1
35\t1
36\t1
37\t1
38\t1
39\t1
40\t1
41\t1
42\t1
43\t1
44\t1
45\t1
46\t1
47\t2
48\t1
49\t1
50\t1
51\t1
52\t1
53\t2
54\t1
55\t1
56\t1
57\t1
58\t1
59\t1
60\t2
61\t1
62\t1
63\t2
64\t2
65\t1
66\t1
67\t1
68\t2
69\t1
70\t1
71\t1
72\t1
73\t1
74\t2
75\t1
76\t1
77\t1
78\t1
79\t1
80\t1
81\t1
82\t1
83\t2
84\t1
85\t1
86\t1
87\t1
88\t1
89\t1
90\t1
91\t1
92\t1
93\t1
94\t1
95\t2
96\t1
97\t2
98\t1
99\t1
100\t2
101\t2
102\t1
"""

txt_niveles_cursos = """id_nivel_curso\tnombre
1\tBasico 1
2\tBasico 2
3\tBasico 3
4\tBasico 4
5\tBasico 5
6\tIntermedio 1
7\tIntermedio 2
8\tIntermedio 3
9\tIntermedio 4
10\tIntermedio 5
12\tIntermedio 6
13\tAvanzado 1
14\tAvanzado 2
15\tAvanzado 3
16\tAvanzado 4
17\tAvanzado 5
18\tAvanzado 6
19\tAvanzado 7
20\tAvanzado 8
"""

# ----- Cargar DataFrames desde texto -----

df_estudiantes = pd.read_csv(StringIO(txt_estudiantes), sep="\t")
df_cursos = pd.read_csv(StringIO(txt_cursos), sep="\t")
df_paquetes = pd.read_csv(StringIO(txt_paquetes), sep="\t")
df_grados = pd.read_csv(StringIO(txt_grados), sep="\t")
df_niveles = pd.read_csv(StringIO(txt_niveles), sep="\t")
df_est_cursos = pd.read_csv(StringIO(txt_estudiantes_cursos), sep="\t")
df_metodos = pd.read_csv(StringIO(txt_metodos), sep="\t")
df_est_metodos = pd.read_csv(StringIO(txt_est_metodos), sep="\t")
df_est_paquetes = pd.read_csv(StringIO(txt_est_paquetes), sep="\t")
df_niveles_cursos = pd.read_csv(StringIO(txt_niveles_cursos), sep="\t")

# ----- Procesar relaciones -----

# Para "curso":
# Renombramos la columna "nombre" del DataFrame de cursos para evitar conflicto
df_cursos.rename(columns={"nombre": "curso_nombre"}, inplace=True)
df_est_cursos["id_curso"] = df_est_cursos["id_curso"].astype(str)
df_cursos["id_curso"] = df_cursos["id_curso"].astype(str)
df_est_cursos = df_est_cursos.merge(df_cursos, on="id_curso", how="left")
df_curso_final = df_est_cursos.groupby("matricula")["curso_nombre"].apply(lambda x: ", ".join(x.dropna().unique())).reset_index()
df_curso_final.rename(columns={"curso_nombre": "curso"}, inplace=True)

# Para "paquete":
df_est_paquetes["id_paquete"] = df_est_paquetes["id_paquete"].astype(str)
df_paquetes["id_paquete"] = df_paquetes["id_paquete"].astype(str)
df_est_paquetes = df_est_paquetes.merge(df_paquetes, on="id_paquete", how="left")
df_paquete_final = df_est_paquetes.groupby("matricula")["nombre"].apply(lambda x: ", ".join(x.dropna().unique())).reset_index()
df_paquete_final.rename(columns={"nombre": "paquete"}, inplace=True)

# Para "metodo_pago":
df_est_metodos["id_metodo"] = df_est_metodos["id_metodo"].astype(str)
df_metodos["id_metodo"] = df_metodos["id_metodo"].astype(str)
df_est_metodos = df_est_metodos.merge(df_metodos, on="id_metodo", how="left")
df_metodo_final = df_est_metodos.groupby("matricula")["nombre"].apply(lambda x: ", ".join(x.dropna().unique())).reset_index()
df_metodo_final.rename(columns={"nombre": "metodo_pago"}, inplace=True)

# ----- Unir toda la información en un solo DataFrame -----

df_final = df_estudiantes.copy()
df_final = df_final.merge(df_curso_final, on="matricula", how="left")
df_final = df_final.merge(df_paquete_final, on="matricula", how="left")
df_final = df_final.merge(df_metodo_final, on="matricula", how="left")

# Mapear claves de grados y niveles a sus descripciones
map_grados = {"1": "Preescolar", "2": "Primaria"}
map_niveles = {"1": "preescolar", "2": "elemental", "3": "ambos"}

df_final["id_grado"] = df_final["id_grado"].astype(str).map(map_grados).fillna(df_final["id_grado"])
df_final["id_nivel_educativo"] = df_final["id_nivel_educativo"].astype(str).map(map_niveles).fillna(df_final["id_nivel_educativo"])

# Agregar columnas adicionales vacías para futura información
columnas_adicionales = ["fecha_nacimiento", "fecha_pago", "monto_pago", "saldo_pendiente"]
for col in columnas_adicionales:
    df_final[col] = ""

# Reordenar columnas
columnas_finales = [
    "matricula", "nombre", "sexo", "fecha_inscripcion", "id_grado", "id_nivel_educativo", "estado_matricula",
    "curso", "paquete", "metodo_pago"
] + columnas_adicionales
df_final = df_final[columnas_finales]

# ----- Guardar el CSV final -----

ruta_csv_final = "alumnos_inblocket_final.csv"
df_final.to_csv(ruta_csv_final, index=False)
print("CSV generado:", ruta_csv_final)
