export interface Cliente {
  id: number;
  nome: string;
  telefone: string;
  email?: string;
  observacao?: string;
}

export interface ClienteCreate {
  nome: string;
  telefone: string;
  email?: string;
  observacao?: string;
}

export interface ClienteUpdate {
  nome?: string;
  telefone?: string;
  email?: string;
  observacao?: string;
}

export interface ClienteListResponse {
  clientes: Cliente[];
  total: number;
} 