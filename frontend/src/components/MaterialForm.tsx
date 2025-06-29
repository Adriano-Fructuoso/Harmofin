import React, { useState, useEffect, useRef } from 'react';
import { Form, Input, InputNumber, Button, Space, message, Switch, Select, Row, Col } from 'antd';
import { SaveOutlined } from '@ant-design/icons';
import { Material, MaterialCreate, MaterialUpdate } from '../types/material';
import { materiaisApi } from '../services/api';

const { Option } = Select;

interface MaterialFormProps {
  material?: Material;
  onSave?: (material: MaterialCreate | MaterialUpdate) => void;
  onCancel?: () => void;
  mode?: 'create' | 'edit';
}

const MaterialForm: React.FC<MaterialFormProps> = ({
  material,
  onSave,
  onCancel,
  mode = 'create'
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [materiais, setMateriais] = useState<Material[]>([]);
  const [camposDesabilitados, setCamposDesabilitados] = useState(false);
  const selectRef = useRef<any>(null);

  useEffect(() => {
    if (material) {
      form.setFieldsValue(material);
    }
  }, [material, form]);

  useEffect(() => {
    carregarMateriais();
  }, []);

  const carregarMateriais = async () => {
    try {
      const response = await materiaisApi.listar({ ativo: true });
      setMateriais(response.data.materiais);
    } catch (error) {
      // Não mostrar erro para não atrapalhar cadastro
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      if (mode === 'create') {
        const materialData: MaterialCreate = {
          nome: values.nome,
          descricao: values.descricao,
          quantidade_disponivel: values.quantidade_disponivel,
          unidade: values.unidade,
          valor_unitario: values.valor_unitario,
          estoque_minimo: values.estoque_minimo,
          ativo: values.ativo !== false
        };
        onSave?.(materialData);
      } else {
        const materialData: MaterialUpdate = {
          nome: values.nome,
          descricao: values.descricao,
          quantidade_disponivel: values.quantidade_disponivel,
          unidade: values.unidade,
          valor_unitario: values.valor_unitario,
          estoque_minimo: values.estoque_minimo,
          ativo: values.ativo !== false
        };
        onSave?.(materialData);
      }
      form.resetFields();
    } catch (error) {
      message.error('Erro ao salvar material');
    } finally {
      setLoading(false);
    }
  };

  // Função para normalizar nome (igual backend)
  function normalizarNome(nome: string): string {
    if (!nome) return '';
    return nome
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  // Gerar lista de nomes únicos ordenados alfabeticamente para o dropdown
  const nomesUnicos = Array.from(new Set(materiais.map(m => m.nome))).sort((a, b) => a.localeCompare(b));

  // Função para preencher campos ao selecionar material existente
  const handleNomeChange = (value: string) => {
    const materialSelecionado = materiais.find(m => m.nome === value);
    if (materialSelecionado) {
      form.setFieldsValue({
        unidade: materialSelecionado.unidade,
        valor_unitario: materialSelecionado.valor_unitario,
        estoque_minimo: materialSelecionado.estoque_minimo,
        descricao: materialSelecionado.descricao || '',
        ativo: materialSelecionado.ativo
      });
      setCamposDesabilitados(true);
    } else {
      // Limpa os campos se for nome novo
      form.setFieldsValue({
        unidade: undefined,
        valor_unitario: undefined,
        estoque_minimo: undefined,
        descricao: '',
        ativo: true
      });
      setCamposDesabilitados(false);
    }
  };

  // Impede scroll bubbling do dropdown
  const handleDropdownVisibleChange = (open: boolean) => {
    if (open) {
      setTimeout(() => {
        const dropdown = document.querySelector('.ant-select-dropdown:not(.ant-select-dropdown-hidden) .rc-virtual-list')?.parentElement;
        if (dropdown) {
          dropdown.addEventListener('wheel', (e: any) => {
            const { scrollTop, scrollHeight, clientHeight } = dropdown;
            const atTop = scrollTop === 0;
            const atBottom = scrollTop + clientHeight === scrollHeight;
            if ((atTop && e.deltaY < 0) || (atBottom && e.deltaY > 0)) {
              e.preventDefault();
            }
          }, { passive: false });
        }
      }, 100);
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={{
        quantidade_disponivel: 0,
        unidade: 'un',
        valor_unitario: 0,
        estoque_minimo: 0,
        ativo: true
      }}
      style={{ marginTop: 8 }}
    >
      <Row gutter={16}>
        <Col xs={24} md={16}>
          <Form.Item
            name="nome"
            label={<span style={{ fontWeight: 500 }}>Nome do Material</span>}
            rules={[{ required: true, message: 'Informe o nome do material' }]}
          >
            <Input placeholder="Digite o nome do material" />
          </Form.Item>
        </Col>
        <Col xs={24} md={8} style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
          <Form.Item
            name="ativo"
            label={<span style={{ fontWeight: 500 }}>Ativo</span>}
            valuePropName="checked"
            style={{ marginBottom: 0 }}
          >
            <Switch />
          </Form.Item>
        </Col>
      </Row>

      <Form.Item
        name="descricao"
        label={<span style={{ fontWeight: 500 }}>Descrição</span>}
      >
        <Input.TextArea rows={2} placeholder="Descrição do material (opcional)" disabled={camposDesabilitados} />
      </Form.Item>

      <Row gutter={16}>
        <Col xs={24} md={6}>
          <Form.Item
            name="quantidade_disponivel"
            label={<span style={{ fontWeight: 500 }}>Quantidade</span>}
            rules={[{ required: true, message: 'Informe a quantidade' }]}
          >
            <InputNumber
              min={0}
              step={0.1}
              precision={2}
              placeholder="0.0"
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Col>
        <Col xs={24} md={6}>
          <Form.Item
            name="unidade"
            label={<span style={{ fontWeight: 500 }}>Unidade</span>}
            rules={[{ required: true, message: 'Informe a unidade' }]}
          >
            <Select
              showSearch
              allowClear
              placeholder="Selecione ou digite a unidade"
              optionFilterProp="children"
              style={{ width: '100%' }}
              disabled={camposDesabilitados}
            >
              <Option value="un">Unidade (un)</Option>
              <Option value="ml">Mililitro (ml)</Option>
              <Option value="mg">Miligrama (mg)</Option>
              <Option value="g">Grama (g)</Option>
              <Option value="kg">Quilograma (kg)</Option>
              <Option value="l">Litro (l)</Option>
              <Option value="cm">Centímetro (cm)</Option>
              <Option value="m">Metro (m)</Option>
              <Option value="caixa">Caixa</Option>
              <Option value="frasco">Frasco</Option>
              <Option value="ampola">Ampola</Option>
              <Option value="seringa">Seringa</Option>
              <Option value="agulha">Agulha</Option>
              <Option value="kit">Kit</Option>
              <Option value="outro">Outro</Option>
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} md={6}>
          <Form.Item
            name="valor_unitario"
            label={<span style={{ fontWeight: 500 }}>Valor Unitário</span>}
            rules={[{ required: true, message: 'Informe o valor' }]}
          >
            <InputNumber
              prefix="R$"
              min={0}
              step={0.01}
              precision={2}
              placeholder="0.00"
              style={{ width: '100%' }}
              disabled={camposDesabilitados}
            />
          </Form.Item>
        </Col>
        <Col xs={24} md={6}>
          <Form.Item
            name="estoque_minimo"
            label={<span style={{ fontWeight: 500 }}>Estoque Mínimo</span>}
            rules={[{ required: true, message: 'Informe o estoque mínimo' }]}
          >
            <InputNumber
              min={0}
              step={0.1}
              precision={2}
              placeholder="0.0"
              style={{ width: '100%' }}
              disabled={camposDesabilitados}
            />
          </Form.Item>
        </Col>
      </Row>

      <Form.Item style={{ textAlign: 'right', marginTop: 16 }}>
        <Space>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={loading}
            icon={<SaveOutlined />}
          >
            {mode === 'create' ? 'Criar Material' : 'Atualizar Material'}
          </Button>
          {onCancel && (
            <Button onClick={onCancel}>
              Cancelar
            </Button>
          )}
        </Space>
      </Form.Item>
    </Form>
  );
};

export default MaterialForm; 