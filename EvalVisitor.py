if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
    from .funxVisitor import funxVisitor
else:
    from funxParser import funxParser
    from funxVisitor import funxVisitor

from antlr4 import *
from funxLexer import funxLexer


# Nota: He passat la practica per el pep8 i se que em dona error en les variables 'l'. Pero en els visitors de les
# transparencies es diuen aixi. Per lo tant, encara que es un nom d'una variable, per mantenir un "standard" amb
# les transparencies ho deixo aixi.
class EvalVisitor(funxVisitor):

    # diccionari per guardar les funcions
    dicFunction = {}
    # diccionari per guardar les variables
    dicVariable = [{}]
    # estructura auxiliar per passar-li al flask
    functionsToDisplay = []

    # Funcio auxiliar per retornar el resultat donat un string (utilitzada en
    # el flask i en les funcions d'ordre superior)
    def Result(self, input_stream):
        input_stream = InputStream(input_stream)
        visitor = self
        lexer = funxLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = funxParser(token_stream)
        tree = parser.root()
        return visitor.visit(tree)

    # Funcio auxiliar per demanar el totes les funcions al flask
    def getFunctions(self):
        return self.functionsToDisplay

    # Funcio auxiliar per aplanar una llista (mes endevant s'explica per que)
    def flatten(self, l):
        if len(l) == 0:
            return []

        if isinstance(l[0], list):
            return self.flatten(l[0]) + self.flatten(l[1:])
        else:
            return [l[0]] + self.flatten(l[1:])

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())

        # Aixo executa declaracions de Funx fins la primera declaracio d'un
        # numero
        for x in l:
            a = self.visit(x)
            if a is not None:
                return a

        return None

    # Expressions del estil: expr operador expr
    def visitExpression(self, ctx):

        op_function_table = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a // b,
            '%': lambda a, b: a % b,
            '^': lambda a, b: a ** b,
            '>': lambda a, b: 1 if a > b else 0,
            '<': lambda a, b: 1 if a < b else 0,
            '>=': lambda a, b: 1 if a >= b else 0,
            '<=': lambda a, b: 1 if a <= b else 0,
            '=': lambda a, b: 1 if a == b else 0,
            '!=': lambda a, b: 1 if a != b else 0,
            '&&': lambda a, b: 1 if a != 0 and b != 0 else 0,
            '||': lambda a, b: 1 if a != 0 or b != 0 else 0,
        }

        l = list(ctx.getChildren())

        a = self.visit(l[0])
        b = self.visit(l[2])
        if isinstance(a, list) or isinstance(b, list):
            raise Exception('Cannot do operations with lists')

        # Operacio aritmetica o logica amb les dos expressions
        return op_function_table[l[1].getText()](a, b)

    # Per assignar valors a variables del estil (ID <- expr o ID {elements})
    # per assignar un numero o una llista
    def visitAssig(self, ctx):
        l = list(ctx.getChildren())
        self.dicVariable[-1][l[0].getText()] = self.visit(l[2])

    # Cosas com !expr o -expr
    def visitBinaryExpr(self, ctx):
        l = list(ctx.getChildren())

        a = self.visit(l[1])
        if isinstance(a, list):
            raise Exception('Cannot do operations with lists')

        if l[0].getText() == '!':
            return 1 if a == 0 else 0

        else:
            return -1 * a

    # Atomic son els "atoms" de les expressions. Quan no es poden descomposar mes
    # Per exemple: 3 + a els atoms son '3' i 'a'
    def visitAtomic(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0])

    # per retornar la expressio de (expr)
    def visitBracket(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    # Asignar elements a les llistes de forma indexada
    # Quan es fa l[i] <- expr
    def visitAssigArray(self, ctx):
        l = list(ctx.getChildren())
        l2 = self.dicVariable[-1][l[0].getText()]

        if not isinstance(l2, list):
            raise Exception('Cannot acces to element if is not a list')
        a = self.visit(l[2])

        if not isinstance(a, int):
            raise Exception(
                'You have to use numbers for access by index to a list')

        b = self.visit(l[5])

        if not isinstance(b, int):
            raise Exception('Lists only accepts integers as element')

        l2[a] = b

    # Gramatica auxiliar que necesitaba per definir els atoms
    def visitNumber(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    # Retornar el valor de una variable normal
    def visitVar(self, ctx):
        l = list(ctx.getChildren())
        return self.dicVariable[-1].get(l[0].getText(), 0)

    # Retornar el valor de un element de la llista (fer l[i])
    def visitElementFromArray(self, ctx):
        l = list(ctx.getChildren())
        l2 = self.dicVariable[-1].get(l[0].getText(), 0)
        if isinstance(l2, list):

            a = self.visit(l[2])
            if not isinstance(a, int):
                raise Exception(
                    'You have to use numbers for access by index to a list')

            return l2[a]

        else:
            raise Exception(l[0].getText() + " is not a list")

    # Crear els elements d'una llista
    def visitElements(self, ctx):
        l = list(ctx.getChildren())

        a = self.visit(l[0])
        print(a)

        if not isinstance(a, int):
            raise Exception('Lists only accepts integers as element')

        if len(l) == 1:
            return [a]

        else:
            # flatten es perque es crea una llista de la forma [a, [b, [c, ...] ] ]
            # i llavors aplanar-la
            return self.flatten([a, self.visit(l[2])])

    # Body es el codi que hi ha dins dels { }
    def visitBody(self, ctx):
        l = list(ctx.getChildren())
        for x in l:
            a = self.visit(x)
            if a is not None:
                return a
        return None

    # if o if + else
    def visitConditional(self, ctx):
        l = list(ctx.getChildren())

        # nomes un if
        if len(l) == 5 and self.visit(l[1]) != 0:
            return self.visit(l[3])

        # if + else
        elif len(l) == 9:
            return self.visit(l[3]) if self.visit(
                l[1]) != 0 else self.visit(l[7])

    # Autoexplicatiu
    def visitLoop(self, ctx):
        l = list(ctx.getChildren())
        while self.visit(l[1]) != 0:
            self.visit(l[3])

    # Funcio Map
    def visitMapFunction(self, ctx):

        l = list(ctx.getChildren())
        if l[1].getText() not in self.dicFunction:
            raise Exception(
                "The function " +
                l[1].getText() +
                " is not declared")

        l2 = self.dicVariable[-1].get(l[2].getText(), 0)

        if not isinstance(l2, list):
            raise Exception('The variable you introduced is not a list')

        if len(self.dicFunction[l[1].getText()][0]) != 1:
            raise Exception(
                'You have to use functions that needs exactly one argument')

        l3 = []

        for x in l2:
            # Es crea aquest string per donar-li al AntLR que ho resolgui
            # (com fer una simulacio de la crida a la funcio per cada element)
            s = l[1].getText() + " " + str(x)
            l3.append(self.Result(s))

        return l3

    # Mateix raonament que Map
    def visitFilterFunction(self, ctx):
        l = list(ctx.getChildren())
        if l[1].getText() not in self.dicFunction:
            raise Exception(
                "The function " +
                l[1].getText() +
                " is not declared")

        l2 = self.dicVariable[-1].get(l[2].getText(), 0)

        if not isinstance(l2, list):
            raise Exception('The variable you introduced is not a list')

        if len(self.dicFunction[l[1].getText()][0]) != 1:
            raise Exception(
                'You have to use functions that needs exactly one argument')

        l3 = []

        for x in l2:
            s = l[1].getText() + " " + str(x)
            res = self.Result(s)
            # Filtre per posar-ho a la nova llista o no
            if res != 0:
                l3.append(x)

        return l3

    # Declaracio d'una funcio
    def visitFunction(self, ctx):
        l = list(ctx.getChildren())
        if l[0].getText() in self.dicFunction:
            raise Exception("This function already exists!")

        # Per guardar els parametres de la funcio
        dicVarFunction = {}
        i = 1
        # Agafar els parametres de la funcio (per aixo comença
        # per i = 1)
        while l[i].getText() != '{':
            r = l[i].getText()
            # Mirar que no s'han repetit noms de parametres
            if r in dicVarFunction:
                raise Exception("The parameter " + r + " is repeated")
            # Donar un valor "default" per fer replace
            dicVarFunction[r] = 0
            i += 1

        # diccionari per les variables de la funcion / body
        l2 = [dicVarFunction, l[len(l) - 2]]
        # Guardar en el diccionari de les funcions
        self.dicFunction[l[0].getText()] = l2

        # Per guardar el nom de la funcio i parametres per donar-li al Flask
        # perque es pugui veure en la web
        s = l[0].getText() + " "
        for key in l2[0]:
            s += key + " "

        self.functionsToDisplay.append(s)

    # Cridar la funcio
    def visitCallfunction(self, ctx):
        l = list(ctx.getChildren())

        if l[0].getText() not in self.dicFunction:
            raise Exception("This function doesn't exist")

        # func[0] es el diccionari de les variables, func[1] es el body
        func = self.dicFunction.get(l[0].getText())

        if len(func[0]) != len(l) - 1:
            raise Exception(
                "This functions does not admit this number of parameters. Please check it")

        # declaracion de las expresiones en las variables

        d = {}

        for x, y in zip(func[0], l[1:]):
            d[x] = self.visit(y)

        self.dicVariable.append(d)

        # llamar al cuerpo con las nuevas variables
        a = self.visit(func[1])

        # devolver las antiguas variables
        self.dicVariable.pop(-1)

        return a
