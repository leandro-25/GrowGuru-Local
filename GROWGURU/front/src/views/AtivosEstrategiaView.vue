<template>
  <ion-page class="ativos-page">
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      
      <ion-header class="ion-no-border">
      <ion-toolbar>
        <div class="header-container">
          <div class="logo-container">
            <img src="@/assets/imagem/logoPPP.png" alt="Logo" class="logo-image" />
            <div class="brand-text">
               <ion-title>{{ estrategiaNome }}</ion-title>
            </div>
          </div>

        </div>
      </ion-toolbar>
    </ion-header>

  <ion-content>
      
    <div class="content-container">
      <div v-if="loading" class="loading-state">
        <ion-spinner></ion-spinner>
        <p>Carregando ativos...</p>
      </div>

      <div v-else-if="ativos.length === 0" class="empty-state">
        <ion-icon :icon="alertCircleOutline" size="large"></ion-icon>
        <p>Nenhum ativo encontrado nesta estratégia</p>
      </div>

    <div class="cards-grid">
      <div v-for="(ativo, index) in ativos" :key="index" class="card-wrapper">
        <ion-card class="ativo-card">
          <div class="card-header">
            <div class="asset-info">
              <div class="asset-details">
                <h3>{{ ativo.ativos.codigo }}</h3>
                <span class="asset-type">{{ formatAssetType(ativo.ativos.tipo) }}</span>
              </div>
            </div>
            <div class="header-actions">
              <ion-button fill="clear" size="small" class="news-button" @click="toggleNewsCard(ativo)">
                <ion-icon :icon="newspaperOutline" slot="icon-only"></ion-icon>
                <span class="button-label">Notícias</span>
              </ion-button>
              <ion-badge class="position-badge">#{{ ativo.posicao }}</ion-badge>
            </div>
          </div>
          <ion-card-content class="card-content">
            <div class="form-row">
              <ion-item class="form-input" style="--min-height: 80px;">
                <ion-label position="floating" style="font-size: 16px; --color: #F9FAFB; transform: none !important; margin-left: 0.1em;">Valor Unitário</ion-label>
                <ion-input
                  :value="ativo.valorCompra"
                  @ionChange="onValorChange($event, ativo)"
                  type="number"
                  :placeholder="ativo.ativos.preco_atual.toFixed(2)"
                  step="0.01"
                  class="custom-input"
                ></ion-input>
              </ion-item>

              <ion-item class="form-input">
                <ion-label position="floating">Quantidade</ion-label>
                <ion-input
                  :value="ativo.quantidade"
                  @ionChange="onQuantidadeChange($event, ativo)"
                  type="number"
                  min="1"
                  class="custom-input"
                ></ion-input>
              </ion-item>
            </div>

            <div class="total-section">
              <span>Total</span>
              <span class="total-amount">R$ {{ calculateTotal(ativo) }}</span>
            </div>

            <ion-button 
              @click="adicionarCarteira(ativo)" 
              expand="block"
              class="buy-button"
            >
              <ion-icon :icon="addCircle" slot="start"></ion-icon>
              Adicionar à Carteira
            </ion-button>
          </ion-card-content>
        </ion-card>
      </div>
      </div>
    </div>
      <!-- Botão flutuante com menu de ações -->
      <div class="floating-actions">
        <button class="fab-button" @click="toggleActions">
          <ion-icon :icon="ellipsisVertical"></ion-icon>
        </button>
        
        <div class="action-buttons" :class="{ 'show-actions': showActions }">
          <button class="action-button" @click="handleRefreshAction">
            <ion-icon :icon="refreshOutline"></ion-icon>
            <span>Atualizar</span>
          </button>
          <button class="action-button" @click="goBack">
            <ion-icon :icon="arrowBackOutline"></ion-icon>
            <span>Voltar</span>
          </button>
        </div>
      </div>
    </ion-content>
    
    <ion-tab-bar slot="bottom" class="custom-tab-bar">
      <ion-tab-button tab="home" href="/tabs/home">
        <ion-icon :icon="homeOutline"></ion-icon>
        <!--<ion-label>Início</ion-label>-->
      </ion-tab-button>

      <ion-tab-button tab="estrategias" href="/tabs/estrategias" class="estrategias-tab-selected">
        <ion-icon :icon="analyticsOutline"></ion-icon>
        <!--<ion-label>Estratégias</ion-label>-->
      </ion-tab-button>

      <ion-tab-button tab="carteira" href="/tabs/carteira">
        <ion-icon :icon="cardOutline"></ion-icon>
        <!--<ion-label>Carteira</ion-label>-->
      </ion-tab-button>
    </ion-tab-bar>
    
  </ion-tabs>
  
  <!-- Card flutuante de notícias -->
  <div v-if="showNewsCard" class="news-card-overlay" @click.self="showNewsCard = false">
    <div class="news-card">
      <div class="news-card-header">
        <h3>Notícias - {{ selectedAtivo?.ativos?.codigo }}</h3>
        <ion-button fill="clear" @click="showNewsCard = false">
          <ion-icon :icon="closeOutline"></ion-icon>
        </ion-button>
      </div>
      <div class="news-card-content">
        <div v-if="loadingNews" class="loading-news">
          <ion-spinner></ion-spinner>
          <p>Buscando notícias...</p>
        </div>
        <div v-else>
          <div class="impact-badge" :class="'impact-' + newsImpact">
            {{ newsImpact === 'positivo' ? 'Positivo' : newsImpact === 'negativo' ? 'Negativo' : 'Neutro' }}
          </div>
          <p>{{ newsContent }}</p>
        </div>
      </div>
    </div>
  </div>
  
  </ion-page>
</template>


<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { api } from '@/api';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonList, IonItem, IonLabel, IonBackButton, IonButtons,
  IonButton, IonIcon, IonBadge, IonSpinner, IonRefresher,
  IonRefresherContent, IonItemSliding, IonInput,
  IonTabs, IonTabBar, IonTabButton
} from '@ionic/vue';
import { toastController } from '@ionic/vue';
import {
  addCircle, alertCircleOutline, ellipsisVertical,
  trendingUpOutline, trendingDownOutline, ticketOutline,
  pricetagOutline, businessOutline, cardOutline,
  homeOutline, analyticsOutline, refreshOutline, arrowBackOutline,
  newspaperOutline, closeOutline, closeCircleOutline
} from 'ionicons/icons';

const route = useRoute();
const router = useRouter();
const estrategiaNome = ref('');
const ativos = ref([]);
const loading = ref(true);
const showActions = ref(false);
const showNewsCard = ref(false);
const selectedAtivo = ref(null);
const loadingNews = ref(false);
const newsContent = ref('');
const newsImpact = ref('neutro');
  
const toggleActions = () => {
  showActions.value = !showActions.value;
};

const toggleNewsCard = async (ativo) => {
  try {
    loadingNews.value = true;
    selectedAtivo.value = ativo;
    showNewsCard.value = true; // Mostrar o card imediatamente com o loading
    
    // Chamar a API para buscar notícias
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3000/api'}/noticias`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        ticker: ativo.ativos.codigo
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Erro ao buscar notícias');
    }
    
    const data = await response.json();
    console.log('Resposta da API:', data); // Log para debug
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    newsContent.value = data.resumo || 'Nenhuma notícia encontrada para este ativo.';
    newsImpact.value = (data.impacto || 'neutro').toLowerCase();
  } catch (error) {
    console.error('Erro ao buscar notícias:', error);
    newsContent.value = 'Não foi possível carregar as notícias no momento.';
    newsImpact.value = 'neutro';
    showNewsCard.value = true;
  } finally {
    loadingNews.value = false;
  }
};

const handleRefreshAction = async (event) => {
  await carregarDados();
  showActions.value = false;
  if (event && event.target) {
    event.target.complete();
  }
};

const goBack = () => {
  router.go(-1);
};

const handleRefresh = handleRefreshAction;

const carregarDados = async () => {
  loading.value = true;
  try {
    const estrategiaId = route.params.id;
    
    // Buscar estratégia e ativos
    const estrategiaResponse = await api.get(`/estrategias?id=eq.${estrategiaId}`);
    const ativosResponse = await api.get(`/estrategias/${estrategiaId}/ativos`);

    estrategiaNome.value = estrategiaResponse.data[0]?.nome || 'Estratégia';
    
    // Inicializar com valores editáveis
    ativos.value = ativosResponse.data.map(a => {
      const precoAtual = a.ativo?.preco_atual || 0;
      return {
        ...a,
        valorCompra: precoAtual, // Valor padrão editável
        quantidade: 1,           // Quantidade padrão editável
        ativos: {                // Garantindo que a estrutura esperada exista
          preco_atual: precoAtual,
          codigo: a.codigo_ativo,
          nome: a.ativo?.nome || '',
          tipo: a.ativo?.tipo || ''
        }
      };
    });
  } catch (error) {
    console.error('Erro:', error);
    mostrarMensagem('Falha ao carregar dados', 'danger');
  } finally {
    loading.value = false;
  }
};

const onValorChange = (event, ativo) => {
  // event.detail.value contém o valor digitado (em string)
  const novoValor = parseFloat(event.detail.value);
  // Atualiza somente se o valor for um número válido
  ativo.valorCompra = isNaN(novoValor) ? ativo.ativos.preco_atual : novoValor;
};

const onQuantidadeChange = (event, ativo) => {
  const novaQtd = parseInt(event.detail.value, 10);
  ativo.quantidade = isNaN(novaQtd) ? 1 : novaQtd;
};

const adicionarCarteira = async (ativo) => {
  try {
    // Utilize os valores que já estão no objeto ativo
    const estrategiaId = parseInt(route.params.id); 
    
    // Validação do ID
    if (isNaN(estrategiaId)) {
      throw new Error('ID da estratégia inválido');
    }

    const valor = ativo.valorCompra;
    const qtd = ativo.quantidade;

    if (isNaN(valor) || valor <= 0) throw new Error('Valor inválido');
    if (isNaN(qtd) || qtd <= 0) throw new Error('Quantidade inválida');

    // Enviar dados para a API e capturar a resposta
    const response = await api.post('/carteira', {
      codigo_ativo: ativo.ativos.codigo,
      quantidade: qtd,
      valor_compra: valor,
      estrategia_id: estrategiaId // Adicionar ID da estratégia
    });

    // Atualizar o saldo localmente se a resposta contiver novo_saldo
    if (response.data && response.data.data) {
      // Emitir evento para atualizar o saldo na HomePage
      if (response.data.data.novo_saldo !== undefined) {
        window.dispatchEvent(new CustomEvent('saldo-atualizado', { 
          detail: { novo_saldo: response.data.data.novo_saldo } 
        }));
      }
      
      // Emitir evento para atualizar a carteira
      window.dispatchEvent(new CustomEvent('carteira-atualizada'));
    }

    // Exibir mensagem de sucesso e resetar os valores para os padrões
    mostrarMensagem(`${qtd} unidade(s) compradas!`, 'success');
    ativo.valorCompra = ativo.ativos.preco_atual;
    ativo.quantidade = 1;
  } catch (error) {
    console.error('Erro na compra:', error);
    mostrarMensagem(error.response?.data?.error || error.message, 'danger');
  }
};

  // Métodos auxiliares para formatação
  const formatCurrency = (value) => {
    return parseFloat(value).toFixed(2).replace('.', ',');
  };

  const formatPercentage = (value) => {
    return `${value > 0 ? '+' : ''}${parseFloat(value).toFixed(2)}%`;
  };

  const formatAssetType = (type) => {
    const types = {
      'acao': 'Ação',
      'fii': 'Fundo Imobiliário',
      'bdr': 'BDR',
      'etf': 'ETF',
      'stock': 'Ação',
      'reit': 'FII',
      'crypto': 'Criptomoeda'
    };
    return types[type.toLowerCase()] || type;
  };

  const getAssetIcon = (type) => {
    const icons = {
      'acao': businessOutline,
      'fii': businessOutline,
      'bdr': cardOutline,
      'etf': trendingUpOutline,
      'stock': businessOutline,
      'reit': businessOutline,
      'crypto': pricetagOutline
    };
    return icons[type.toLowerCase()] || pricetagOutline;
  };

  const getPriceChangeIcon = (value) => {
    return value >= 0 ? trendingUpOutline : trendingDownOutline;
  };

  const calculateTotal = (ativo) => {
    const total = ativo.valorCompra * ativo.quantidade;
    return isNaN(total) ? '0,00' : formatCurrency(total);
  };

const mostrarMensagem = async (mensagem, cor) => {
  const toast = await toastController.create({
    message: mensagem,
    duration: 3000,
    color: cor,
    position: 'top'
  });
  await toast.present();
};

onMounted(() => {
  carregarDados();
});
</script>

<style lang="scss" scoped>
@import '@/theme/ativos-estrategia.scss';

/* Estilo da tab bar para ficar igual ao TabsLayout.vue */
ion-tab-bar {
  --background: #111827; /* Fundo Principal */
  --color: #F9FAFB; /* Texto Principal */
  --border-color: #374151; /* Divisores e Bordas */
  padding: 5px 0;
  height: 60px;
}

ion-tab-button {
  --color: #a0aec0; /* Cor padrão do ícone/label (cinza claro) */
  --color-selected: #F59E0B; /* Acentos e Destaques (Âmbar) */
  --background-focused: rgba(245, 158, 11, 0.1); /* Fundo sutil ao focar */
  position: relative;
  overflow: visible;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 6px;
  height: 100%;
}

ion-tab-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 50%;
  height: 3px;
  background: #F59E0B;
  transition: transform 0.3s ease;
  border-radius: 0 0 4px 4px;
}

/* Estilo para a tab ativa */
ion-tab-button.tab-selected::before {
  transform: translateX(-50%) scaleX(1);
}
</style>
