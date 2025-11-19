# MiniCalc-Compiler
DOCUMENTACION

1. Descripción General del Compilador
He creado un compilador simple llamado MiniCalc Compiler en Python (lenguaje de preferencia, ya que es fácil de prototipar y ejecutar). Este compilador traduce un pequeño lenguaje de programación llamado MiniCalc (definido a continuación) a código intermedio en forma de instrucciones de tres direcciones (un formato simple y común para representaciones intermedias en compiladores).
Características implementadas:

a. Analizador Léxico: Tokeniza el código fuente en tokens (palabras clave, identificadores, números, operadores, etc.).
b. Analizador Sintáctico: Usa un parser recursivo descendente para analizar la sintaxis y construir un Árbol de Sintaxis Abstracta (AST).
c. Analizador Semántico (Opcional): Verifica tipos básicos (solo números enteros) y asegura que las variables estén declaradas antes de usarlas. Reporta errores semánticos.
d. Generar Tabla de Símbolos: Mantiene una tabla de símbolos para rastrear variables declaradas, sus tipos y valores (si se asignan).
e. Generador de Código Intermedio: Convierte el AST en instrucciones de tres direcciones (t1 = a + b).
f. Lenguaje de programación a traducir: El compilador traduce MiniCalc (el lenguaje fuente) a código intermedio (no a un lenguaje ejecutable final, para mantenerlo simple). Si se desea, se puede extender para generar código Python o ensamblador.

Herramientas utilizadas: Solo Python estándar (sin bibliotecas externas). El compilador es un script único (minicalc_compiler.py) que puedes ejecutar desde la línea de comandos.
Limitaciones: Es un compilador muy básico para expresiones aritméticas simples. No soporta bucles, condicionales complejos, funciones, etc. Está diseñado para ser educativo y extensible.

2. Lenguaje de Programación: MiniCalc
MiniCalc es un lenguaje simple para expresiones aritméticas con variables. Su gramática es la siguiente (en notación EBNF simplificada):
	Programa: Una secuencia de declaraciones.
	Declaración: var <identificador> = <expresión>; (declara y asigna una variable) | <identificador> = <expresión>; (asigna a una variable existente).
	Expresión: <término> ((+ | -) <término>)*
	Término: <factor> ((* | /) <factor>)*
	Factor: <número> | <identificador> | (<expresión>)
	Identificador: Secuencia de letras (e.g., a, var1).
	Número: Entero positivo (e.g., 5, 42).

Ejemplos de código MiniCalc válido:
var x = 5;
var y = x + 3 * 2;
z = y - 1;
Ejemplos de código inválido:
	x = 5; (sin declarar x primero).
	var 123 = 5; (identificador inválido).
	var x = a + b; (variables no declaradas).

Pruebas recomendadas:
	Código válido: var a = 10; var b = a * 2; c = b + 5;
	Código con error léxico: var @a = 10;
	Código con error sintáctico: var a = 10 + ;
	Código con error semántico: b = a + 1; (sin declarar a).
	

3. Código Fuente del Compilador
Aquí está el código completo en Python. Guárdalo en un archivo llamado minicalc_compiler.py. Es un script ejecutable que toma un archivo de entrada con código MiniCalc y genera el código intermedio.
python295 lines
Copy codeDownload code
Click to expand
import sys
import re

4. Cómo Ejecutar el Compilador
	Requisitos: Python  instalado.
	Ejecución:
•	Crea un archivo de texto con código MiniCalc (e.g., input.mc con var x = 5; var y = x + 3;).
•	Ejecuta: python minicalc_compiler.py input.mc.
	Salida: Código intermedio (e.g., x = 5, t1 = x + 3, y = t1) y tabla de símbolos.
	Ejecutable: El script es el "ejecutable". Para un .exe, usa PyInstaller: pip install pyinstaller; pyinstaller --onefile minicalc_compiler.py.

5. Documentación del Compilador
	Arquitectura: El compilador sigue las fases estándar: léxico → sintáctico → semántico → generación de código intermedio.
	Errores: Reporta errores léxicos, sintácticos y semánticos con mensajes claros.
	Extensibilidad: Agrega soporte para más operadores o estructuras modificando las clases.
	Pruebas: Usa los ejemplos de MiniCalc arriba. Para errores, prueba código inválido.
