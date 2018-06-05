class Error:
	def __init__(self, tipo): 
		self.errors = {"tokenInesperado" : "Token inesperado", "fimArquivo" : "chegou no fim do arquivo"}
		if tipo in self.errors:
			print(self.errors[tipo])
		elif:
			print("Erro não identificado")
		

		