<template>
  <ion-page class="estrategias-page">
    <ion-header class="ion-no-border">
      <ion-toolbar>
        <div class="header-container">
          <div class="logo-container">
            <img src="@/assets/imagem/logoP.png" alt="Logo" class="logo-image" />
            <div class="brand-text">
              <span class="brand-bold">Estratégias</span>
            </div>
          </div>
        </div>
      </ion-toolbar>
    </ion-header>


    
    <ion-content 
      ref="content" 
      class="ion-padding"
      :scroll-events="true"
    >
      <!-- Filtro de Tipo de Estratégia -->
      <div class="filtro-container">
        <ion-select 
          v-model="filtroTipo" 
          placeholder="Filtrar por tipo" 
          interface="action-sheet"
          class="filtro-select"
          @ionChange="aplicarFiltro"
        >
          <ion-select-option value="">Todas as estratégias</ion-select-option>
          <ion-select-option 
            v-for="tipo in tiposEstrategias" 
            :key="tipo" 
            :value="tipo"
          >
            {{ tipo }}
          </ion-select-option>
        </ion-select>
      </div>
      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content
          pulling-icon="chevron-down-circle-outline"
          refreshing-spinner="circles"
        ></ion-refresher-content>
      </ion-refresher>

      <!-- Loading State -->
      <div v-if="loading" class="loading-indicator">
        <ion-spinner></ion-spinner>
        <p>Carregando...</p>
      </div>

      <div class="content-container" :class="{ 'content-loading': loading }">
        <!-- Empty State -->
        <div v-if="!loading && !estrategias.length" class="empty-state">
          <ion-icon :icon="documentTextOutline" class="empty-icon"></ion-icon>
          <p>Nenhuma estratégia encontrada</p>
        </div>
        <div class="estrategias-grid">
        <div 
          v-for="estrategia in estrategiasFiltradas" 
          :key="estrategia.id"
          class="estrategia-card"
        >
          <div class="card-header">
            <div class="header-content">
              <h3 class="estrategia-nome">{{ estrategia.nome }}</h3>
            </div>
            <div class="estrategia-data">
              <ion-icon :icon="calendarOutline"></ion-icon>
              <span>{{ formatarData(estrategia.created_at) }}</span>
            </div>
          </div>

          <div class="card-content">
            <div class="descricao-container">
              <p class="estrategia-descricao">
                <strong>Risco:</strong> {{ estrategia.descricao || 'Nenhuma descrição fornecida' }}
              </p>
            </div>
            
            <div class="detalhes-container">
              <div class="metrica">
                <div class="metrica-rotulo">
                  <div class="metrica-icone" :class="getRentabilidadeClass(estrategia.rentabilidade_media)">
                    <ion-icon :icon="trendingUpOutline"></ion-icon>
                  </div>
                  <span>Rentabilidade Média</span>
                </div>
                <span class="metrica-valor" :class="getRentabilidadeClass(estrategia.rentabilidade_media, true)">
                  {{ formatRentabilidade(estrategia.rentabilidade_media) }}
                </span>
              </div>
              
              <div class="metrica">
                <div class="metrica-rotulo">
                  <div class="metrica-icone">
                    <ion-icon :icon="briefcaseOutline"></ion-icon>
                  </div>
                  <span>Ativos Relacionados</span>
                </div>
                <span class="badge-ativos">
                  {{ estrategia.total_ativos || 0 }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <button 
              class="botao-acao"
              @click.stop="verDetalhes(estrategia.id)"
            >
              <span>Ver Detalhes</span>
              
            </button>
          </div>
        </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonCard, IonCardHeader, IonCardTitle, IonCardSubtitle,
  IonCardContent, IonText, IonList, IonItem, IonLabel,
  IonNote, IonButton, IonIcon, IonSpinner, IonBadge,
  IonRefresher, IonRefresherContent, IonButtons, IonSelect, IonSelectOption
} from '@ionic/vue';
import {
  arrowForwardCircle,
  calendarOutline,
  trendingUpOutline,
  briefcaseOutline,
  refreshOutline,
  documentOutline
} from 'ionicons/icons';

const router = useRouter();
const estrategias = ref([]);
const estrategiasFiltradas = ref([]);
const loading = ref(true);
const filtroTipo = ref('');
const tiposEstrategias = ref([]);

// Format functions
const formatarData = (dataISO) => {
  return new Date(dataISO).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });
};

const formatRentabilidade = (valor) => {
  if (!valor) return 'N/A';
  return `${valor.toFixed(2)}%`;
};

const getRentabilidadeColor = (valor) => {
  if (!valor) return 'medium';
  return valor >= 0 ? 'success' : 'danger';
};

const getRentabilidadeClass = (valor, isValue = false) => {
  if (isValue) {
    return valor >= 0 ? 'positive-value' : 'negative-value';
  }
  return valor >= 0 ? 'positive-value' : 'negative-value';
};

// Actions
const verDetalhes = (id) => {
  router.push({ 
    name: 'AtivosEstrategia',
    params: { id }
  });
};

const handleRefresh = async (event) => {
  await carregarEstrategias();
  event.target.complete();
};

const refreshEstrategias = () => {
  loading.value = true;
  carregarEstrategias();
};

const carregarEstrategias = async () => {
  try {
    const { data } = await api.get('/estrategias');
    estrategias.value = data;
    
    // Extrai os tipos únicos de estratégias
    const tiposUnicos = [...new Set(data.map(e => e.tipo_estrategia).filter(Boolean))];
    tiposEstrategias.value = tiposUnicos.sort();
    
    // Aplica o filtro inicial
    aplicarFiltro();
  } catch (error) {
    console.error('Erro ao carregar estratégias:', error);
  } finally {
    loading.value = false;
  }
};

const aplicarFiltro = () => {
  if (!filtroTipo.value) {
    estrategiasFiltradas.value = [...estrategias.value];
  } else {
    estrategiasFiltradas.value = estrategias.value.filter(
      estrategia => estrategia.tipo_estrategia === filtroTipo.value
    );
  }
};

onMounted(() => {
  carregarEstrategias();
});
</script>

<style lang="scss">
@use '@/theme/estrategias';


</style>