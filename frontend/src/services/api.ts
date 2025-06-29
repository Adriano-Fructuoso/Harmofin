import axios from 'axios';
import { 
  Cliente, ClienteListResponse, 
  Atendimento, AtendimentoList, AtendimentoCreate, AtendimentoUpdate
} from '../types/atendimento';
import { 
  Material, MaterialListResponse, MaterialCreate, MaterialUpdate, MaterialEstoqueBaixo 
} from '../types/material';
import {
  Procedimento, ProcedimentoListResponse, ProcedimentoCreate, ProcedimentoUpdate
} from '../types/procedimento';

// Usar proxy do Vite em vez de URL direta
const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Clientes
export const clientesApi = {
  listar: () => api.get<ClienteListResponse>('/clientes'),
  buscar: (termo: string) => api.get<ClienteListResponse>(`/clientes/busca?termo=${termo}`),
  obter: (id: number) => api.get<Cliente>(`/clientes/${id}`),
  criar: (cliente: Omit<Cliente, 'id' | 'data_cadastro'>) => api.post<Cliente>('/clientes', cliente),
  atualizar: (id: number, cliente: Partial<Cliente>) => api.put<Cliente>(`/clientes/${id}`, cliente),
  remover: (id: number) => api.delete(`/clientes/${id}`),
};

// Atendimentos
export const atendimentosApi = {
  listar: (params?: {
    skip?: number;
    limit?: number;
    cliente_id?: number;
    procedimento_id?: number;
    data_inicio?: string;
    data_fim?: string;
    status?: string;
  }) => api.get<AtendimentoList>('/atendimentos', { params }),
  obter: (id: number) => api.get<Atendimento>(`/atendimentos/${id}`),
  criar: (atendimento: AtendimentoCreate) => api.post<Atendimento>('/atendimentos', atendimento),
  atualizar: (id: number, atendimento: AtendimentoUpdate) => api.put<Atendimento>(`/atendimentos/${id}`, atendimento),
  remover: (id: number) => api.delete(`/atendimentos/${id}`),
  estatisticas: () => api.get<{
    total_atendimentos: number;
    atendimentos_hoje: number;
    atendimentos_mes: number;
    valor_total_mes: number;
  }>('/atendimentos/estatisticas/resumo'),
};

// Procedimentos
export const procedimentosApi = {
  listar: (params?: { skip?: number; limit?: number; ativo?: boolean }) => 
    api.get<ProcedimentoListResponse>('/procedimentos', { params }),
  obter: (id: number) => api.get<Procedimento>(`/procedimentos/${id}`),
  criar: (procedimento: ProcedimentoCreate) => 
    api.post<Procedimento>('/procedimentos', procedimento),
  atualizar: (id: number, procedimento: ProcedimentoUpdate) => 
    api.put<Procedimento>(`/procedimentos/${id}`, procedimento),
  remover: (id: number) => api.delete(`/procedimentos/${id}`),
  materiaisPadrao: (id: number) => api.get(`/procedimentos/${id}/materiais-padrao`),
};

// Materiais
export const materiaisApi = {
  listar: (params?: { skip?: number; limit?: number; ativo?: boolean; estoque_baixo?: boolean }) =>
    api.get<MaterialListResponse>('/materiais', { params }),
  
  obter: (id: number) =>
    api.get<Material>(`/materiais/${id}`),
  
  criar: (material: MaterialCreate) =>
    api.post<Material>('/materiais', material),
  
  atualizar: (id: number, material: MaterialUpdate) =>
    api.put<Material>(`/materiais/${id}`, material),
  
  remover: (id: number) =>
    api.delete(`/materiais/${id}`),
  
  estoqueBaixo: () =>
    api.get<MaterialListResponse>('/materiais/estoque/baixo'),
  
  buscarSimilares: (nome: string, threshold?: number) =>
    api.get('/materiais/buscar/similares', { 
      params: { nome, threshold: threshold || 0.8 } 
    }),
  
  criarOuBuscar: (material: MaterialCreate) =>
    api.post<Material>('/materiais/criar-ou-buscar', material),

  ajustarEstoque: (id: number, quantidade: number, tipo: 'entrada' | 'saida') =>
    api.post(`/materiais/${id}/ajustar-estoque`, null, {
      params: { quantidade, tipo }
    })
};

export default api; 