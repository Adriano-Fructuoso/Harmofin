import React, { useState, useEffect } from 'react';
import { Select, Input, Button, Card, Space, message, Modal, Form, InputNumber } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import { Material } from '../types/material';
import { materiaisApi } from '../services/api';

const { Option } = Select;

interface MaterialSelectorProps {
  value?: number;
  onChange?: (value: number) => void;
  placeholder?: string;
  style?: React.CSSProperties;
  allowCreate?: boolean;
  onMaterialCreated?: (material: Material) => void;
}

const MaterialSelector: React.FC<MaterialSelectorProps> = ({
  value,
  onChange,
  placeholder = "Selecione ou digite um material",
  style,
  allowCreate = true,
  onMaterialCreated
}) => {
  const [materiais, setMateriais] = useState<Material[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchValue, setSearchValue] = useState('');
  const [similares, setSimilares] = useState<Material[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    carregarMateriais();
  }, []);

  const carregarMateriais = async () => {
    try {
      setLoading(true);
      const response = await materiaisApi.listar({ ativo: true });
      setMateriais(response.data.materiais);
    } catch (error) {
      message.error('Erro ao carregar materiais');
    } finally {
      setLoading(false);
    }
  };

  const buscarSimilares = async (nome: string) => {
    if (!nome || nome.length < 2) {
      setSimilares([]);
      return;
    }

    try {
      const response = await materiaisApi.buscarSimilares(nome);
      setSimilares(response.data.materiais_similares || []);
    } catch (error) {
      console.error('Erro ao buscar similares:', error);
      setSimilares([]);
    }
  };

  const handleSearch = (value: string) => {
    setSearchValue(value);
    buscarSimilares(value);
  };

  const handleCreateMaterial = async (values: any) => {
    try {
      setLoading(true);
      const response = await materiaisApi.criarOuBuscar({
        nome: values.nome,
        descricao: values.descricao,
        quantidade_disponivel: values.quantidade_disponivel || 0,
        unidade: values.unidade || 'un',
        valor_unitario: values.valor_unitario || 0,
        estoque_minimo: values.estoque_minimo || 0
      });

      const novoMaterial = response.data;
      
      // Adicionar à lista de materiais
      setMateriais(prev => [...prev, novoMaterial]);
      
      // Selecionar o novo material
      if (onChange) {
        onChange(novoMaterial.id);
      }

      if (onMaterialCreated) {
        onMaterialCreated(novoMaterial);
      }

      setModalVisible(false);
      form.resetFields();
      message.success('Material criado com sucesso!');
      
      // Recarregar materiais para garantir sincronização
      await carregarMateriais();
      
    } catch (error) {
      message.error('Erro ao criar material');
    } finally {
      setLoading(false);
    }
  };

  const renderOptions = () => {
    const options = [];

    // Adicionar materiais similares primeiro
    if (similares.length > 0) {
      options.push(
        <Option key="similares-header" disabled>
          📋 Materiais similares encontrados:
        </Option>
      );
      
      similares.forEach(material => {
        options.push(
          <Option key={`similar-${material.id}`} value={material.id}>
            {material.nome} (Estoque: {material.quantidade_disponivel} {material.unidade})
          </Option>
        );
      });
      
      options.push(<Option key="divider-1" disabled>──────────</Option>);
    }

    // Adicionar todos os materiais
    materiais.forEach(material => {
      const isSimilar = similares.some(s => s.id === material.id);
      if (!isSimilar) {
        options.push(
          <Option key={material.id} value={material.id}>
            {material.nome} (Estoque: {material.quantidade_disponivel} {material.unidade})
          </Option>
        );
      }
    });

    return options;
  };

  return (
    <>
      <Select
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        style={style}
        loading={loading}
        showSearch
        onSearch={handleSearch}
        filterOption={false}
        dropdownRender={(menu) => (
          <div>
            {menu}
            {allowCreate && searchValue && (
              <div style={{ padding: '8px', borderTop: '1px solid #f0f0f0' }}>
                <Button
                  type="dashed"
                  icon={<PlusOutlined />}
                  onClick={() => setModalVisible(true)}
                  style={{ width: '100%' }}
                >
                  Criar "{searchValue}"
                </Button>
              </div>
            )}
          </div>
        )}
      >
        {renderOptions()}
      </Select>

      <Modal
        title="Criar Novo Material"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateMaterial}
          initialValues={{
            nome: searchValue,
            quantidade_disponivel: 0,
            unidade: 'un',
            valor_unitario: 0,
            estoque_minimo: 0
          }}
        >
          <Form.Item
            name="nome"
            label="Nome do Material"
            rules={[{ required: true, message: 'Informe o nome do material' }]}
          >
            <Input placeholder="Ex: Toxina Botulínica" />
          </Form.Item>

          <Form.Item
            name="descricao"
            label="Descrição"
          >
            <Input.TextArea rows={2} placeholder="Descrição do material (opcional)" />
          </Form.Item>

          <Space>
            <Form.Item
              name="quantidade_disponivel"
              label="Quantidade Disponível"
              rules={[{ required: true, message: 'Informe a quantidade' }]}
            >
              <InputNumber
                min={0}
                step={0.1}
                precision={2}
                placeholder="0.0"
                style={{ width: 120 }}
              />
            </Form.Item>

            <Form.Item
              name="unidade"
              label="Unidade"
              rules={[{ required: true, message: 'Informe a unidade' }]}
            >
              <Input placeholder="un" style={{ width: 80 }} />
            </Form.Item>
          </Space>

          <Space>
            <Form.Item
              name="valor_unitario"
              label="Valor Unitário"
              rules={[{ required: true, message: 'Informe o valor' }]}
            >
              <InputNumber
                prefix="R$"
                min={0}
                step={0.01}
                precision={2}
                placeholder="0.00"
                style={{ width: 120 }}
              />
            </Form.Item>

            <Form.Item
              name="estoque_minimo"
              label="Estoque Mínimo"
              rules={[{ required: true, message: 'Informe o estoque mínimo' }]}
            >
              <InputNumber
                min={0}
                step={0.1}
                precision={2}
                placeholder="0.0"
                style={{ width: 120 }}
              />
            </Form.Item>
          </Space>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>
                Criar Material
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                Cancelar
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default MaterialSelector; 