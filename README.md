
# Funx

Benvingut a FUNX!. Un simple llenguatge de programació interpretat amb Python y fet amb ANTLR. 
Aquesta versió ha sigut creada per Alex Herrero.



## Executar Funx

Cóm executar Funx? 

Una vegada descarregat tots els arxius executa la comanda per primer cop:

```bash
  antlr4 -Dlanguage=Python3 -no-listener -visitor funx.g4 && export FLASK_APP=funx
```
I cada vegada què es vulgui executar executa


```bash
  flask run
```
Quan s'hagin ficat aquestes comandes (si ```flask ``` no dona error) llavors el interpret
estarà preparat en la direcció IP què surt per la terminal. 

## L'interpret de Funx

La UI de Funx es veu així:

![Logo](https://cdn.discordapp.com/attachments/964517229150498846/1057004038912217088/image.png)

En ella es poden apreciar els següents elements:
+ Editor de text: En ell es pot escriure codi de Funx i es pot executar per veure el resultat
+ Results: Aquí es veuen les ultimes 5 entrades què l'usuari ha executat i el seu Output. Si per lo què fos l'usuari cometés un error (divisó per zero, paràmetres no correctes...) llavors se li informa al usuari en el output.
+ Functions: Aquí es poden veure totes les funcions què l'usuari ha guardat en la seva execució de Funx. 

## Com és el llenguatge de Funx

Funx és un llenguatge creat per els professors de la asignatura de Llenguatges de Programació
de la FIB en el Q1-2022/23. Això és la exposició del treball així que si es vol sapiguer com funciona
tot el llenguatge de Funx us podeu dirigir la [presentació del llenguatge](https://github.com/gebakx/lp-funcions#presentaci%C3%B3-del-llenguatge)
i també la [especificació del llenguatge](https://github.com/gebakx/lp-funcions#especificaci%C3%B3-de-funx).


## A més a més...

S'han agregat les següents funcionalitats a aquest projecte de Funx per fer-ho més flexible
### Operadors lògics
S'han agregat els operadors lògics:
+ L'operador `&&`per indicar la AND 
+ L'operador `||`per indicar la OR 
+ L'operador `!`per indicar la NOT

Tots tres amb un funcionament totalment identics al dels llenguatges de programació com C, retornant 1 en cas de ser certa la condició o 0 en cas de ser falsa.
Faig un recordatori de que en Funx agafem com "True" tot el que no sigui zero i, obviament, agafem zero com "False". Encara que tots els operador lògics 
retornen 1 en cas de cert i 0 en cas de fals.

El proposit de l'agregació d'aquests operadors és per poguer fer Funx més flexible a l'hora de fer condicionals.

Per exemple:

```bash
if a != b && c = d { #Do something } 
```
s'executarà només sí `a` és diferent a `b` i quan `c` és igual a `d`.


```bash
if a != b || c = d { #Do something } 
```
Aquest codi s'executarà si `a` és diferent a `b` o quan `c` sigui igual a `d`.

```bash
if !(a != b && c = d) { #Do something }
```
I per acabar aquest codi s'executa quan no es cumpleixi la condició de dins (és a dir: quan `a`sigui igual a `b` o quan `c`sigui diferent a `d`). És important recalcar que quan es vulgui utilitzar el operador Not en una expressió es faci amb els parentesis a aquesta, si no el not agafarà i li pot fer el Not només a la primera variable.


Si no s'hagues afegit aquesta condició, el primer exemple -per posar algun- es tindria que fer així en el funx tradicional:

```bash
if a != b { if c = d { #Something }}
```
Lo qual es pot simplificar com hem vist al primer exemple. Potser "encara" es podria arribar a fer la operació AND amb 2 if's encadenats. Mirem com es faria la OR sense l'operador:
```bash
if a != b { #Do something } if c = d { #Do the same}
```

Si el codi arribes a ser llarg seria realment molt pesat per arribar-ho a llegir. Més amb Funx que no està pensat, en un principi, per fer codis llargs..
### Llistes

També s'ha extendid Funx amb Llistes. Les llistes de Funx tenen un comportament molt semblant a les llistes de Python.

El funcionament de les llistes en Funx es:

```bash
#Per crear una llista

l  {a,b,c,d,e,...}
```
Així creem una llista de nom `l`amb elements a,b,c,d,e... Els elements tenen que ser números
(o be retornar números). Així per exemple si definim una funció `Dos`que retorna un 2, una variable `a`de valor 4
podem crear una llista de la forma 


```bash
l {Dos, a, 4*6}
```

Y crear una llista amb elements 2, 4 y 24. És important recalcar què es tenen que posar números o bé expressions o bé crides a funcions que retornin números. En cap momento es tindrien què acceptar coses com if's,whiles... Com a paràmetres per a crear la llista.

També es pot accedir al i-ésim element de la llista amb la notació estandard que segueixen els arrays de C o les propies 
llistes de Python per exemple. També igual què es pot accedir es pot modificar el valor d'aquella posició amb l'operador <- de Funx.

```bash
#Accedir i-esim element de una llista l
l[i]
#Amb i desde zero fins n-1

#Modificar valor:
l[i] <- 3
#Aixi modifiquem l'i-essim element amb el valor 3 per exemple
```
També podem demanar a Funx què ens doni tots els elements de la llista i ho fa igual que si li demanem el contigut d'una variable

S'ha decidit agregar aquesta aquesta estructura de dades perquè és un eina realment molt útil què es troba en la gran majoria de llenguatges de programació.
És important remarcar què aquestes llistes han sigut pensades per ser 1-Dimensional, no es permeten llistes multi-dimensionals.
### Funció Map

Perquè com diu Gerard Escudero: "La gràcia de la part de Python de LP és utilitzar la programació funcional
que s'havia après amb Haskell" (o com vem adaptar en el meu grup d'amics "la gràcia de la vida residueix a les funcions d'ordre superior de Python") . Així que la "classica" funció Map què es troba en Python o Haskell també s'ha agregat a Funx.
La sintaxis que segueix és la següent:


```bash
Map Nom_Funció Nom_Llista
```

I el funcionament és analog a la funció de Map de Python o Haskell: Donada una funció f i una llista l
{a,b,c,d,e...} retorna la llista {f(a), f(b), f(c), f(d), f(e),...}. Com Funx ha sigut creat amb la idea de fer
llistes 1-Dimensionals les funcions què admet aquesta funció només poden ser d'un argument. 

### Funció filter

Totalmente anàloga a la funció de Map, mateixa sintaxis amb mateixos errors.
La sintaxis que segueix és la següent:


```bash
Filter Nom_Funció Nom_Llista
```

I el funcionament és analog a la funció de Map de Python o Haskell: Donada una funció, aquesta "filtra" els elements de la llista segons si la funció retorna zero o no. Un exemple podria ser aquest:


```bash
Filter even l
```

On l es una llista declarada como {1,2,3,4} i even es una funció que, donat un número, retorna zero si no es parell. Llavors la llista al final queda {2,4}


## Agraiments

* Agraiments al professor Gerard Escudero què ha sigut una gran ajuda en l'aprenentatge de la part de compiladors de la asignatura de LP. Podeu llegir les transparencies què m'han sigut d'ajuda [aqui](https://gebakx.github.io/Python3/compiladors.html#1). La pràctica ha sigut, com deia ell en els laboratoris, feta "amb carinyo".
* També al meu amic [Víctor](https://github.com/hectobreak) que ja va cursar l'asignatura de LP quan jo estic en ella i m'ha resolt tots els dubtes que he tingut sobre la pràctica (i sobre altres assigntures)

