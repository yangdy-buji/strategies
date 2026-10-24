import unittest
from tests.safe_expression import evaluate

class SafeExpressionTests(unittest.TestCase):
    def test_numeric_boolean_and_list_cases(self):
        self.assertEqual(evaluate('entry - atr * ratio',entry=100,atr=2,ratio=3),94)
        self.assertEqual(evaluate('close[1] - low[1]',close=[0,101],low=[0,100]),1)
        self.assertTrue(evaluate('start <= time and time <= end',start=1,time=2,end=3))
        self.assertFalse(evaluate('not enabled or value > 3',enabled=True,value=2))
    def test_rejects_calls_attributes_and_complex_objects(self):
        for text in ['().__class__.__bases__','__import__("os")','x.__class__','[x for x in y]','lambda: 1','2 ** 10000000']:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):evaluate(text,x=1,y=[1])
        with self.assertRaises(ValueError):evaluate('x',x=object())
        with self.assertRaises(ValueError):evaluate('x * 1000000000',x=[1,2])

if __name__=='__main__':unittest.main()
