# -*- coding: utf-8 -*-
from clusters.clusterfeatures import ClusterFeatures
from dados.daoarquivo import DAOarquivo
from sklearn.cluster import KMeans
import numpy as np
from algoritimosclustering.simplekmeans import SimpleKmeansPython
from algoritimosclustering.simplekmeansmake import SimplePassKmeans
from algoritimosclustering.birch import BirchAlgo
from algoritimosclustering.leader import TheLeaderAlgorithm
from helper.funcoesaux import preencherClusters
from helper.funcoesaux import pegaClustersOrganizados
from helper.funcoesaux import criaTexto

class Gerenciador(object):
    """
        Classe responsável por gerenciar as funções necessárias
        Basicamente para não explicitar todas as funções existentes na main
    """
    daoIO = None
    executa = False
    simple_kmeans = None
    sp_kmeans = None
    birch = None
    leader = None
    marjorityvoting = None

    def __init__(self, caminho):
        self.daoIO = DAOarquivo(caminho)

    def inicia(self, num_cluster, threshholdBirch, thresholdLeader):
        self.simple_kmeans = SimpleKmeansPython(num_cluster)
        self.sp_kmeans = SimplePassKmeans(num_cluster)
        self.birch = BirchAlgo(threshold=threshholdBirch)
        self.leader = TheLeaderAlgorithm(threshold=thresholdLeader)
    

    # Responsável por iniciar os dados vindo do csv
    def iniciaDataset(self, particao_final = 10):
        self.daoIO.LerArquivo()
        self.daoIO.calcula_particao(particao_final)
        self.daoIO.inicia_dados()
        self.simple_kmeans.verdadeira_estatistica(self.daoIO.dados)
        if(particao_final > 1 or particao_final == 0):
            self.executa = True


    def novoDataStream(self, randon):
        if randon:
            self.executa = self.daoIO.cria_aleatorio()
            self.simple_kmeans.atualiza_kmeans(self.daoIO.randon_data)
            self.sp_kmeans.aplica_kmeans(self.daoIO.randon_data)
            self.birch.aplica_birch(self.daoIO.randon_data)
            self.leader.aplica_leader(self.daoIO.randon_data)
        else:
            self.executa = self.daoIO.pega_particao()
            self.simple_kmeans.aplica_kmeans(self.daoIO.particao)
            # Baseado no do amiguinho
            self.sp_kmeans.aplica_kmeans(self.daoIO.particao)
            #BIRCH
            self.birch.aplica_birch(self.daoIO.particao)
            #The Leader alghortm
            self.leader.aplica_leader(self.daoIO.particao)
        # self.criarCluster()

    def criarCluster(self, randon):

        if randon:
        #Kmeans do scitlearn
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.randon_data, self.simple_kmeans.labels_temporary, self.simple_kmeans.centers)
            preencherClusters(dadosOrganizados, self.simple_kmeans)

            #Kmeans baseado de um codigo na internet
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.randon_data, self.sp_kmeans.labels, self.sp_kmeans.centers)
            preencherClusters(dadosOrganizados, self.sp_kmeans)

            #Birch do scitlearn
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.randon_data, self.birch.labels, self.birch.centers)
            preencherClusters(dadosOrganizados, self.birch)

            #Leader baseado em um algoritimo na internet
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.randon_data, self.leader.labels, self.leader.centers)
            preencherClusters(dadosOrganizados, self.leader)
        else:
            #Kmeans do scitlearn
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.particao, self.simple_kmeans.labels_temporary, self.simple_kmeans.centers)
            preencherClusters(dadosOrganizados, self.simple_kmeans)

            #Kmeans baseado de um codigo na internet
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.particao, self.sp_kmeans.labels, self.sp_kmeans.centers)
            preencherClusters(dadosOrganizados, self.sp_kmeans)

            #Birch do scitlearn
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.particao, self.birch.labels, self.birch.centers)
            preencherClusters(dadosOrganizados, self.birch)

            #Leader baseado em um algoritimo na internet
            dadosOrganizados = pegaClustersOrganizados(self.daoIO.particao, self.leader.labels, self.leader.centers)
            preencherClusters(dadosOrganizados, self.leader)
    

    # Aplica o kmeans no conjunto de dados
    def iniciar(self, randon):
        # kmeans biblioteca do python
        if randon:
            self.simple_kmeans.aplica_kmeans(self.daoIO.randon_data)
            # Baseado no do amiguinho
            self.sp_kmeans.inicia_kmeans(self.daoIO.randon_data)
            self.sp_kmeans.aplica_kmeans(self.daoIO.randon_data)
            #BIRCH
            self.birch.aplica_birch(self.daoIO.randon_data)
            #The Leader alghortm
            self.leader.aplica_leader(self.daoIO.randon_data)
        else:
            self.simple_kmeans.aplica_kmeans(self.daoIO.particao)
            # Baseado no do amiguinho
            self.sp_kmeans.inicia_kmeans(self.daoIO.particao)
            self.sp_kmeans.aplica_kmeans(self.daoIO.particao)
            #BIRCH
            self.birch.aplica_birch(self.daoIO.particao)
            #The Leader alghortm
            self.leader.aplica_leader(self.daoIO.particao)


    def mostraEstatisticas(self):
        self.simple_kmeans.estatisticas()

    def num_cluster(self, caminho):
        num = self.daoIO.LerArquivo(caminho)
        return num.values

    def finalizador(self, dataset):
        texto = criaTexto(self.simple_kmeans.clusters, "Simple pass K-Means " + dataset)
        self.daoIO.salvaArquivo(texto, "SimplePassKMeans " + dataset, "dados/mock/" + dataset + "/")

        texto = criaTexto(self.sp_kmeans.clusters, "Simple pass K-Means Example" + dataset)
        self.daoIO.salvaArquivo(texto, "SimplePassKMeansExample " + dataset, "dados/mock/" + dataset + "/")

        texto = criaTexto(self.birch.clusters, "BIRCH " + dataset)
        self.daoIO.salvaArquivo(texto, "BIRCH " + dataset, "dados/mock/" + dataset + "/")

        texto = criaTexto(self.leader.clusters, "The Leader " + dataset)
        self.daoIO.salvaArquivo(texto, "TheLeader " + dataset, "dados/mock/" + dataset + "/")
