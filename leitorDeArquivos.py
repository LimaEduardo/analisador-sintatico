import sys
from pathlib import Path

class leitorDeFluxo:
	def __init__(self, nomeArquivo):
		self.arquivo = Path(nomeArquivo)
		self.fluxoDeTokens = []

		if self.arquivo.exists():
			self.arquivo = open(nomeArquivo, "r")
			self.fluxoDeTokens = [x.replace('>,','>') for x in self.arquivo.read().split(" ")]
			del self.fluxoDeTokens[-1]
		else:
			print("Arquivo não existe")
			sys.exit()

if __name__ == "__main__":
	fluxo  = leitorDeFluxo("fluxoDeTokens").fluxoDeTokens
	print(fluxo)
