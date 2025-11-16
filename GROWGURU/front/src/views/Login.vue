<template>
  <ion-page class="login-page">
    <ion-content>
      <div class="login-container">
        <div class="login-box">
          <div class="logo-wrapper">
            <img 
              src="@/assets/imagem/logo.png" 
              alt="GrowGuru" 
            />
          </div>
          <h2 class="title">Entre na sua conta</h2>

          <form @submit.prevent="handleLogin" @keyup.enter="handleLogin" class="login-form">
            <!-- Email Input -->
            <div class="form-group">
              <label>Endereço de email</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="email"
                  type="email"
                  placeholder="Insira seu e-mail..."
                  @blur="validateEmail"
                  autocomplete="email"
                  inputmode="email"
                  required
                ></ion-input>
              </div>
              <ion-text v-if="emailError" class="error-message">{{ emailError }}</ion-text>
            </div>

            <!-- Password Input -->
            <div class="form-group">
              <label>Senha</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Insira sua senha..."
                  @blur="validatePassword"
                  autocomplete="current-password"
                  required
                ></ion-input>
                <div 
                  @click="showPassword = !showPassword"
                  class="toggle-password"
                >
                  <ion-icon 
                    :icon="showPassword ? eyeOffOutline : eyeOutline" 
                  ></ion-icon>
                </div>
              </div>
              <ion-text v-if="passwordError" class="error-message">{{ passwordError }}</ion-text>
            </div>

            <!-- Remember Me -->
            <div class="remember-section">
              <div class="remember-checkbox">
                <ion-checkbox v-model="rememberMe"></ion-checkbox>
                <span>Lembrar</span>
              </div>

              <router-link to="/forgot-password" class="forgot-link">
                Esqueceu sua senha?
              </router-link>
            </div>

            <!-- Login Button -->
            <button
              type="submit"
              :disabled="loading || !isValidForm"
              class="submit-button"
            >
              <ion-spinner v-if="loading" name="crescent"></ion-spinner>
              <span>{{ loading ? 'Entrando...' : 'Entrar' }}</span>
            </button>

            <!-- Sign Up Link -->
            <div class="signup-container">
              <p>
                Não tem uma conta? 
                <router-link to="/signup" class="signup-link">
                  Inscrever-se
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </ion-content>
    
    <!-- Toast para exibir mensagens de erro -->
    <ion-toast
      :is-open="toast.show"
      :message="toast.message"
      :color="toast.color"
      :duration="3000"
      @didDismiss="toast.show = false"
    ></ion-toast>
  </ion-page>
</template>

<style lang="scss">
@import '@/theme/login.scss';
</style>



<script setup lang="ts">
import { ref, computed, onMounted, reactive, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonItem, IonLabel, IonInput, IonButton, IonText,
  IonSpinner, IonToast, IonCheckbox, IonIcon
} from '@ionic/vue';
import { eyeOutline, eyeOffOutline } from 'ionicons/icons';

declare global {
  interface Window {
    Capacitor?: {
      isNativePlatform: boolean;
      getPlatform(): string;
    };
  }
}

const email = ref('');
const password = ref('');
const loading = ref(false);
const emailError = ref('');
const passwordError = ref('');
const showPassword = ref(false);
const rememberMe = ref(false);
const toast = reactive({
  show: false,
  message: '',
  color: 'primary'
});
const router = useRouter();

// Load saved email if remember me was used
onMounted(() => {
  const savedEmail = localStorage.getItem('rememberedEmail');
  if (savedEmail) {
    email.value = savedEmail;
    rememberMe.value = true;
  }
});

// Form validation
const isValidForm = computed(() => {
  return email.value && 
         password.value && 
         !emailError.value && 
         !passwordError.value;
});

// Enhanced login handler
const handleLogin = async () => {
  validateEmail();
  validatePassword();
  
  if (!email.value || !password.value) {
    toast.show = true;
    toast.message = 'Por favor, preencha todos os campos';
    toast.color = 'danger';
    return;
  }

  loading.value = true;
  toast.show = false;

  try {
    const { data } = await api.post('/login', {
      email: email.value.trim().toLowerCase(),
      password: password.value
    });
  
    if (rememberMe.value) {
      localStorage.setItem('rememberedEmail', email.value);
    } else {
      localStorage.removeItem('rememberedEmail');
    }
  
    console.log('Token recebido:', data.session.access_token);
    localStorage.setItem('token', data.session.access_token);
    
    toast.show = true;
    toast.message = 'Login successful!';
    toast.color = 'success';
    
    // Força uma atualização no estado de autenticação
    if (window.dispatchEvent) {
      window.dispatchEvent(new Event('storage'));
    }
    
    // Pequeno atraso para garantir que o token seja processado
    setTimeout(() => {
      console.log('Iniciando processo de redirecionamento...');
      
      // Verifica se está em um ambiente Capacitor (Android/iOS)
      const isCapacitor = window.Capacitor && window.Capacitor.isNativePlatform;
      console.log('Ambiente Capacitor:', isCapacitor);
      
      if (isCapacitor) {
        console.log('Dispositivo móvel detectado, usando window.location...');
        window.location.href = '/tabs/home';
      } else {
        console.log('Navegador web, usando router.push...');
        router.push('/tabs/home')
          .catch(() => {
            console.log('Redirecionamento com router falhou, tentando window.location...');
            window.location.href = '/tabs/home';
          });
      }
    }, 300);
  } catch (error: any) {
    // Sempre exibe a mensagem em português para erros de login
    const errorMessage = 'E-mail ou senha incorretos';
    
    // Exibindo a mensagem de erro no toast
    toast.show = true;
    toast.message = errorMessage;
    toast.color = 'danger';
  } finally {
    loading.value = false;
  }
};

const validateEmail = () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  emailError.value = !email.value ? 'Email is required' : !emailPattern.test(email.value) ? 'Invalid email' : '';
};

const validatePassword = () => {
  passwordError.value = !password.value ? 'Password is required' : password.value.length < 6 ? 'Password must be at least 6 characters' : '';
};
</script>
