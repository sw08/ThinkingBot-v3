import re
import utils.errors as errors


class Expression:
    def __init__(self, expression):
        self.terms = sorted(
            [
                Term(i)
                for i in expression.replace(" ", "")
                .replace("-", "+-")
                .replace("+x", "+1x")
                .replace("-x", "-1x")
                .replace("x+", "x^1+")
                .split("+")
            ],
            reverse=True,
            key=lambda x: x.degree,
        )

    def substitute(self, x):
        total = Fraction(0)
        for i in self.terms:
            total += i.substitute(x)
        if total.deno == 1:
            return total.nume
        return total

    def __str__(self):
        terms = []
        for i in self.terms:
            term = "" if i.coefficient.nume > 0 else "- "
            if int(i.coefficient.deno) == 1:
                term += str(abs(i.coefficient.nume))
            else:
                term += f"({abs(i.coefficient.nume)}/{i.coefficient.deno})"
            if i.degree > 0:
                term += "x" if i.degree == 1 else f"x^{i.degree}"
            terms.append(term)
        expression = (" + ".join(terms)).replace("+ -", "-").replace("1x", "x")
        return expression

    @classmethod
    def from_terms(cls, terms):
        expression = cls.__new__(cls)
        expression.terms = terms
        return expression


class Term:
    def __init__(self, term):
        if "x" in term:
            if term[-1] == "x":
                term += "^1"
            splitted = term.split("x^")
            self.degree = int(splitted[1])
            self.coefficient = Fraction(splitted[0])
        else:
            self.degree = 0
            self.coefficient = Fraction(term)

    def substitute(self, x):
        return self.coefficient * (Fraction(x) ** self.degree)

    def __str__(self):
        return (
            f"({self.coefficient.nume}/{self.coefficient.deno})x^{self.degree}".replace(
                "(-", "-("
            )
        )


class Fraction:
    def __init__(self, num):
        num = str(num)
        p1 = re.compile("[-]?[(][0-9]+/[0-9]+[)]")
        p2 = re.compile("[-]?[0-9]+")
        if p1.match(num) is not None:  # fraction
            splitted = num.split("/")
            splitted[0] = splitted[0].replace("-(", "-")
            self.deno = int(splitted[1][:-1])
            self.nume = int(splitted[0])
            if self.deno == 0:
                raise errors.FractionDenoZero
        elif p2.match(num) is not None:  # integer
            self.deno = 1
            self.nume = int(num)
        else:  # wrong
            raise errors.WrongExpression

    def copy(self):
        return Fraction(
            str(self.nume)
            if self.deno == 1
            else f"({self.nume}/{self.deno})".replace("(-", "-(")
        )

    def simplify(self):
        a = abs(self.nume)
        b = abs(self.deno)
        while (a != 1 and b != 1) and a * b != 0:
            a = a % b
            if a < b:
                a, b = b, a
        if a != 1 and b != 1:  # gcd exists
            self.nume /= a
            self.deno /= a
        if self.deno < 0:
            self.nume *= -1
            self.deno *= -1
        self.nume = int(self.nume)
        self.deno = int(self.deno)

    def __str__(self):
        return f"({self.nume}/{self.deno})".replace("(-", "-(")

    def __pow__(self, other):
        temp = self.copy()
        temp.nume **= other
        temp.deno **= other
        return temp

    def __isub__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        if type(other) == int:
            other = Fraction(other)
        other.nume *= -1
        temp += other
        return temp

    def __iadd__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        if temp.deno != other.deno:
            temp.nume *= other.deno
            temp.nume += temp.deno * other.nume
            temp.deno *= other.deno
        else:
            temp.nume += other.nume
        self.simplify()
        return temp

    def __imul__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp.deno *= other.deno
        temp.nume *= other.nume
        temp.simplify()
        return temp

    def __itruediv__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp.deno *= other.nume
        temp.nume *= other.deno
        temp.simplify()
        return temp

    def __add__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp += other
        return temp

    def __sub__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp -= other
        return temp

    def __mul__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp *= other
        return temp

    def __truediv__(self, other):
        temp = self.copy()
        if type(other) == int:
            other = Fraction(other)
        temp /= other
        return temp
