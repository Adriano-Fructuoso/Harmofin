export interface Cliente {
  id: number;
  nome: string;
  telefone: string;
  email?: string;
  observacao?: string;
  data_cadastro: string;
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

export interface Procedimento {
  id: number;
  nome: string;
  descricao?: string;
  valor_padrao: number;
  ativo: boolean;
  data_cadastro: string;
}

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

export interface AtendimentoMaterial {
  id: number;
  material_id: number;
  quantidade_utilizada: number;
  valor_unitario_momento: number;
  material: Material;
}

export interface AtendimentoProcedimento {
  id: number;
  procedimento_id: number;
  valor_cobrado: number;
  observacoes?: string;
  procedimento: Procedimento;
}

export interface Atendimento {
  id: number;
  cliente_id: number;
  procedimento_id: number;
  data_hora: string;
  valor_cobrado: number;
  observacoes?: string;
  status: string;
  data_cadastro: string;
  cliente: Cliente;
  procedimento: Procedimento;
  procedimentos: AtendimentoProcedimento[];
  materiais_utilizados: AtendimentoMaterial[];
}

export interface AtendimentoMaterialCreate {
  material_id: number;
  quantidade_utilizada: number;
  valor_unitario_momento: number;
}

export interface AtendimentoProcedimentoCreate {
  procedimento_id: number;
  valor_cobrado: number;
  observacoes?: string;
}

export interface AtendimentoCreate {
  cliente_id: number;
  procedimento_id: number;
  procedimentos: AtendimentoProcedimentoCreate[];
  data_hora: string;
  valor_cobrado: number;
  observacoes?: string;
  status?: string;
  materiais_utilizados?: AtendimentoMaterialCreate[];
}

export interface AtendimentoUpdate {
  cliente_id?: number;
  procedimento_id?: number;
  data_hora?: string;
  valor_cobrado?: number;
  observacoes?: string;
  status?: string;
}

export interface AtendimentoList {
  atendimentos: Atendimento[];
  total: number;
}

export interface ProcedimentoList {
  procedimentos: Procedimento[];
  total: number;
}

export interface MaterialList {
  materiais: Material[];
  total: number;
}

export interface ClienteListResponse {
  clientes: Cliente[];
  total: number;
} 