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

export interface ProcedimentoMaterial {
  id: number;
  material_id: number;
  quantidade_padrao: number;
  material: Material;
}

export interface Procedimento {
  id: number;
  nome: string;
  descricao?: string;
  valor_padrao: number;
  ativo: boolean;
  data_cadastro: string;
  materiais_padrao: ProcedimentoMaterial[];
}

export interface ProcedimentoCreate {
  nome: string;
  descricao?: string;
  valor_padrao: number;
  ativo?: boolean;
  materiais_padrao?: ProcedimentoMaterialCreate[];
}

export interface ProcedimentoUpdate {
  nome?: string;
  descricao?: string;
  valor_padrao?: number;
  ativo?: boolean;
  materiais_padrao?: ProcedimentoMaterialCreate[];
}

export interface ProcedimentoMaterialCreate {
  material_id: number;
  quantidade_padrao: number;
}

export interface ProcedimentoListResponse {
  procedimentos: Procedimento[];
  total: number;
} 