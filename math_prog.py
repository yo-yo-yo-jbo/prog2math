from typing import Union

class LatexExpr(object):
    """
        Latex expression.
    """

    def __init__(self, expression:Union[str, float]):
        """
            Creates an instance.
        """

        # Save the expression
        self._expression = str(expression)

    def get_expression(self) -> str:
        """
            Gets the expression.
        """

        # Return the expression
        return self._expression

    def __repr__(self) -> str:
        """
            Returns the expression.
        """

        # Return the expression
        return self.get_expression()

class Indicator(LatexExpr):
    """
        An indicator of a condition, should yield 0 or 1 only.
    """

    def __init__(self, expression:str):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(expression)

    @staticmethod
    def logical_and(*indicators:list['Indicator']) -> 'Indicator':
        """
            Creates a new indicator that indicates the logical and of other indicators.
        """

        # Validations
        assert len(indicators) > 0, Exception('Must provide at least one indicator')

        # Create a new indicator by means of multiplication
        return Indicator(''.join([ fr'\left({ind}\right)' for ind in indicators ]))

    @staticmethod
    def logical_not(indicator:'Indicator') -> 'Indicator':
        """
            Creates a new indicator that indicates the negation of the given indicator.
        """

        # Yield a new indicator
        return Indicator(fr'1-\left({indicator}\right)')

    @staticmethod
    def logical_or(*indicators:list['Indicator']) -> 'Indicator':
        """
            Creates a new indicator that indicates the logical or of other indicators.
        """

        # Validations
        assert len(indicators) > 0, Exception('Must provide at least one indicator')

        # Create a new indicator by de Morgan's laws
        return Indicator.logical_not(Indicator.logical_and(*map(Indicator.logical_not, indicators)))

    @staticmethod
    def are_not_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for inequality of two expressions.
        """

        # Use the arctan function and normalize it to indicate inequality
        return Indicator(r'\left\lceil\frac{4\arctan^2{\left(' + f'{a}-{b}' + r'\right)}}{\pi^2}\right\rceil')

    @staticmethod
    def are_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator of equality of two expressions.
        """

        # Use the inequality indicator
        return Indicator.logical_not(Indicator.are_not_equal(a, b))

    @staticmethod
    def is_non_negative(a:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for the given expression being non-negative.
        """

        # Check equality of the expression and its absolute value
        abs_val_expr = LatexExpr(r'\sqrt{' + f'{a}^2' + r'}')
        return Indicator.are_equal(abs_val_expr, a)

    @staticmethod
    def less_than_or_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator of a <= b.
        """

        # Use the non-negativity indicator
        return Indicator.is_non_negative(LatexExpr(f'{b}-{a}'))

    @staticmethod
    def less_than(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a < b.
        """

        # Use the negation of a >= b
        return Indicator.logical_not(Indicatorless_than_or_equal(b, a))

    @staticmethod
    def bigger_than_or_equal(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a >= b.
        """

        # Switch roles
        return Indicator.less_than_or_equal(b, a)

    @staticmethod
    def bigger_than(a:LatexExpr, b:LatexExpr) -> 'Indicator':
        """
            Creates an indicator for a > b.
        """

        # Switch roles
        return Indicator.less_than(b, a)

    @staticmethod
    def is_integer(a:LatexExpr) -> 'Indicator':
        """
            Indicates whether the given expression is an integer.
        """

        # Use the cosine function's period
        return Indicator(fr'\left\lfloor\cos^2\left(\pi {a}\right)\right\rfloor')

    @staticmethod
    def is_natural(a:LatexExpr, include_zero:bool=False) -> 'Indicator':
        """
            Indicates whether the given expression is a natural number (starting from either 0 or 1 as indicated).
        """

        # Use integer checking along a comparison
        natural_cond = Indicator.is_non_negative(a) if include_zero else Indicator.bigger_than(a, LatexExpr(0))
        return Indicator.logical_and(Indicator.is_integer(a), Indicator. natural_cond)
