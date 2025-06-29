import React, { useState, useEffect } from 'react';
import { 
  Table, Card, Button, Space, Tag, Modal, message, Input, Select, 
  InputNumber, Form, Tooltip, Progress 
} from 'antd';
import { 
  EditOutlined, DeleteOutlined, PlusOutlined, InboxOutlined, 
  ExclamationCircleOutlined, WarningOutlined 
} from '@ant-design/icons';
import { materiaisApi } from '../services/api';
import { Material } from '../types/material';

const { Option } = Select;

interface MaterialTableProps {
  onEdit?: (material: Material) => void;
  onDelete?: (id: number) => void;
  onNew?: () => void;
  refresh?: number;
  onEstoqueAjustado?: () => void;
}

const MaterialTable: React.FC<MaterialTableProps> = ({
  onEdit,
  onDelete,
  onNew,
  refresh,
  onEstoqueAjustado
}) => {
  const [materiais, setMateriais] = useState<Material[]>([]);
  const [loading, setLoading] = useState(false);
  const [filtros, setFiltros] = useState({
    ativo: undefined as boolean | undefined,
    estoque_baixo: undefined as boolean | undefined
  });
  const [ajusteModalVisible, setAjusteModalVisible] = useState(false);
  const [materialSelecionado, setMaterialSelecionado] = useState<Material | null>(null);
  const [ajusteForm] = Form.useForm();
  const [ajustandoEstoque, setAjustandoEstoque] = useState(false);

  useEffect(() => {
    carregarDados();
  }, [filtros, refresh]);

  const carregarDados = async () => {
    try {
      setLoading(true);
      const response = await materiaisApi.listar(filtros);
      setMateriais(response.data.materiais);
    } catch (error) {
      message.error('Erro ao carregar materiais');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: 'Confirmar exclusão',
      content: 'Tem certeza que deseja excluir este material?',
      okText: 'Sim',
      cancelText: 'Não',
      onOk: async () => {
        try {
          await materiaisApi.remover(id);
          message.success('Material removido com sucesso');
          carregarDados();
        } catch (error) {
          message.error('Erro ao remover material');
        }
      }
    });
  };

  const handleAjusteEstoque = (material: Material) => {
    setMaterialSelecionado(material);
    setAjusteModalVisible(true);
    ajusteForm.resetFields();
  };

  const handleSubmitAjuste = async (values: any) => {
    if (!materialSelecionado) return;

    try {
      setAjustandoEstoque(true);
      await materiaisApi.ajustarEstoque(
        materialSelecionado.id, 
        values.quantidade, 
        values.tipo
      );
      message.success('Estoque ajustado com sucesso');
      setAjusteModalVisible(false);
      
      // Atualizar imediatamente
      await carregarDados();
      if (onEstoqueAjustado) {
        await onEstoqueAjustado();
      }
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao ajustar estoque');
    } finally {
      setAjustandoEstoque(false);
    }
  };

  const getEstoqueStatus = (material: Material) => {
    const percentual = (material.quantidade_disponivel / material.estoque_minimo) * 100;
    
    if (material.quantidade_disponivel <= material.estoque_minimo) {
      return { status: 'exception', color: 'red', text: 'Crítico' };
    } else if (percentual <= 150) {
      return { status: 'warning', color: 'orange', text: 'Baixo' };
    } else {
      return { status: 'success', color: 'green', text: 'Normal' };
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Material',
      dataIndex: 'nome',
      key: 'nome',
      render: (nome: string, record: Material) => (
        <div>
          <div><strong>{nome}</strong></div>
          {record.descricao && (
            <div style={{ fontSize: '12px', color: '#666' }}>{record.descricao}</div>
          )}
        </div>
      ),
    },
    {
      title: 'Estoque',
      key: 'estoque',
      render: (_: any, record: Material) => {
        const status = getEstoqueStatus(record);
        const percentual = (record.quantidade_disponivel / record.estoque_minimo) * 100;
        
        return (
          <div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ fontWeight: 'bold' }}>
                {record.quantidade_disponivel} {record.unidade}
              </span>
              {status.status === 'exception' && (
                <ExclamationCircleOutlined style={{ color: 'red', marginLeft: 8 }} />
              )}
            </div>
            <Progress 
              percent={Math.min(percentual, 100)} 
              status={status.status as any}
              size="small"
              showInfo={false}
            />
            <div style={{ fontSize: '12px', color: '#666', marginTop: 2 }}>
              Mín: {record.estoque_minimo} {record.unidade}
            </div>
          </div>
        );
      },
    },
    {
      title: 'Valor Unit.',
      dataIndex: 'valor_unitario',
      key: 'valor_unitario',
      render: (valor: number) => `R$ ${valor.toFixed(2)}`,
      sorter: (a: Material, b: Material) => a.valor_unitario - b.valor_unitario,
    },
    {
      title: 'Valor Total',
      key: 'valor_total',
      render: (_: any, record: Material) => {
        const valorTotal = record.quantidade_disponivel * record.valor_unitario;
        return `R$ ${valorTotal.toFixed(2)}`;
      },
      sorter: (a: Material, b: Material) => 
        (a.quantidade_disponivel * a.valor_unitario) - (b.quantidade_disponivel * b.valor_unitario),
    },
    {
      title: 'Status',
      dataIndex: 'ativo',
      key: 'ativo',
      render: (ativo: boolean, record: Material) => {
        const estoqueStatus = getEstoqueStatus(record);
        
        return (
          <Space direction="vertical" size="small">
            <Tag color={ativo ? 'green' : 'red'}>
              {ativo ? 'Ativo' : 'Inativo'}
            </Tag>
            {estoqueStatus.status === 'exception' && (
              <Tag color="red" icon={<WarningOutlined />}>
                Estoque Crítico
              </Tag>
            )}
          </Space>
        );
      },
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 200,
      render: (_: any, record: Material) => (
        <Space>
          <Tooltip title="Ajustar Estoque">
            <Button
              type="primary"
              size="large"
              icon={<InboxOutlined />}
              onClick={() => handleAjusteEstoque(record)}
              title="Ajustar Estoque"
            />
          </Tooltip>
          {onEdit && (
            <Button
              type="default"
              size="large"
              icon={<EditOutlined />}
              onClick={() => onEdit(record)}
              title="Editar"
            />
          )}
          {onDelete && (
            <Button
              type="default"
              size="large"
              danger
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record.id)}
              title="Excluir"
            />
          )}
        </Space>
      ),
    },
  ];

  return (
    <>
      <Card 
        title="Controle de Estoque" 
        extra={
          onNew && (
            <Button type="primary" icon={<PlusOutlined />} onClick={onNew}>
              Novo Material
            </Button>
          )
        }
      >
        {/* Filtros */}
        <div style={{ marginBottom: 16 }}>
          <Space wrap>
            <Select
              placeholder="Status"
              allowClear
              style={{ width: 120 }}
              onChange={(value) => setFiltros(prev => ({ ...prev, ativo: value }))}
            >
              <Option value={true}>Ativo</Option>
              <Option value={false}>Inativo</Option>
            </Select>

            <Select
              placeholder="Estoque"
              allowClear
              style={{ width: 150 }}
              onChange={(value) => setFiltros(prev => ({ ...prev, estoque_baixo: value }))}
            >
              <Option value={true}>Estoque Baixo</Option>
              <Option value={false}>Estoque Normal</Option>
            </Select>

            <Button onClick={() => setFiltros({ ativo: undefined, estoque_baixo: undefined })}>
              Limpar Filtros
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={materiais}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => 
              `${range[0]}-${range[1]} de ${total} materiais`,
          }}
        />
      </Card>

      {/* Modal de Ajuste de Estoque */}
      <Modal
        title={`Ajustar Estoque - ${materialSelecionado?.nome}`}
        open={ajusteModalVisible}
        onCancel={() => setAjusteModalVisible(false)}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={ajusteForm}
          layout="vertical"
          onFinish={handleSubmitAjuste}
        >
          <Form.Item
            name="tipo"
            label="Tipo de Ajuste"
            rules={[{ required: true, message: 'Selecione o tipo de ajuste' }]}
          >
            <Select placeholder="Selecione o tipo">
              <Option value="entrada">Entrada (Compra/Reposição)</Option>
              <Option value="saida">Saída (Consumo/Perda)</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="quantidade"
            label="Quantidade"
            rules={[{ required: true, message: 'Insira a quantidade' }]}
          >
            <InputNumber
              min={0.01}
              step={0.01}
              style={{ width: '100%' }}
              placeholder="0.00"
            />
          </Form.Item>

          <Form.Item
            name="observacao"
            label="Observação (Opcional)"
          >
            <Input.TextArea rows={3} placeholder="Motivo do ajuste..." />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={ajustandoEstoque}>
                Confirmar Ajuste
              </Button>
              <Button onClick={() => setAjusteModalVisible(false)} disabled={ajustandoEstoque}>
                Cancelar
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default MaterialTable; 