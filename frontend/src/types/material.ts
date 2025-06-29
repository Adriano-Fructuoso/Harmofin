export interface Material {
  id: number;
  nome: string;
  descricao?: string;
  quantidade_disponivel: number;
  unidade: string;
  valor_unitario: number;
  estoque_minimo: number;
  ativo: boolean;
  data_cadastro: string;
}

export interface MaterialCreate {
  nome: string;
  descricao?: string;
  quantidade_disponivel: number;
  unidade: string;
  valor_unitario: number;
  estoque_minimo: number;
  ativo?: boolean;
}

export interface MaterialUpdate {
  nome?: string;
  descricao?: string;
  quantidade_disponivel?: number;
  unidade?: string;
  valor_unitario?: number;
  estoque_minimo?: number;
  ativo?: boolean;
}

export interface MaterialListResponse {
  materiais: Material[];
  total: number;
}

export interface AjusteEstoque {
  quantidade: number;
  tipo: 'entrada' | 'saida';
  observacao?: string;
}

export interface MaterialEstoqueBaixo {
  materiais: Material[];
  total: number;
} 