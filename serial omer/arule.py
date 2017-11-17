class Association_Rule:
    def __init__(self,a,b,support,confidence,lift):
        self.a = a
        self.b = b
        self.support = support
        self.confidence = confidence
        self.lift = lift
        
    def __str__(self):
        output = "{0}->{1},support={2:.2f},confidence={3:.2f},lift={4:.2f}".format(str(self.a),str(self.b),self.support,
                                                                    self.confidence,self.lift)
        return output