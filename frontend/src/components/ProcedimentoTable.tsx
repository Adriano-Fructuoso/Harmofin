import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Tag, Popconfirm, message, Card } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, MedicineBoxOutlined } from '@ant-design/icons';
import { Procedimento } from '../types/procedimento';
import { procedimentosApi } from '../services/api';

interface ProcedimentoTableProps {
  onNew: () => void;
  onEdit: (procedimento: Procedimento) => void;
  onDelete: (id: number) => void;
  refresh: number;
}

const ProcedimentoTable: React.FC<ProcedimentoTableProps> = ({
  onNew,
  onEdit,
  onDelete,
  refresh
}) => {
  const [procedimentos, setProcedimentos] = useState<Procedimento[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  const carregarProcedimentos = async (page = 1, pageSize = 10) => {
    try {
      setLoading(true);
      const skip = (page - 1) * pageSize;
      const response = await procedimentosApi.listar({
        skip,
        limit: pageSize
      });
      
      setProcedimentos(response.data.procedimentos);
      setTotal(response.data.total);
      setPagination(prev => ({
        ...prev,
        current: page,
        total: response.data.total,
      }));
    } catch (error) {
      message.error('Erro ao carregar procedimentos');
      console.error('Erro ao carregar procedimentos:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarProcedimentos(pagination.current, pagination.pageSize);
  }, [refresh]);

  const handleTableChange = (pagination: any) => {
    carregarProcedimentos(pagination.current, pagination.pageSize);
  };

  const handleDelete = async (id: number) => {
    try {
      await onDelete(id);
      carregarProcedimentos(pagination.current, pagination.pageSize);
    } catch (error) {
      console.error('Erro ao excluir procedimento:', error);
    }
  };

  const columns = [
    {
      title: 'Nome',
      dataIndex: 'nome',
      key: 'nome',
      render: (text: string) => (
        <div style={{ fontWeight: 'bold' }}>
          <MedicineBoxOutlined style={{ marginRight: 8, color: '#1890ff' }} />
          {text}
        </div>
      ),
    },
    {
      title: 'Descrição',
      dataIndex: 'descricao',
      key: 'descricao',
      render: (text: string) => text || '-',
      ellipsis: true,
    },
    {
      title: 'Valor Padrão',
      dataIndex: 'valor_padrao',
      key: 'valor_padrao',
      render: (valor: number) => (
        <span style={{ fontWeight: 'bold', color: '#52c41a' }}>
          R$ {valor.toFixed(2)}
        </span>
      ),
    },
    {
      title: 'Materiais Padrão',
      key: 'materiais_padrao',
      render: (record: Procedimento) => (
        <div>
          {record.materiais_padrao && record.materiais_padrao.length > 0 ? (
            <div>
              {record.materiais_padrao.slice(0, 2).map((mp, index) => (
                <Tag key={index} color="blue" style={{ marginBottom: 4 }}>
                  {mp.material?.nome || 'Material não encontrado'} ({mp.quantidade_padrao})
                </Tag>
              ))}
              {record.materiais_padrao.length > 2 && (
                <Tag color="blue">+{record.materiais_padrao.length - 2} mais</Tag>
              )}
            </div>
          ) : (
            <span style={{ color: '#999' }}>Nenhum material padrão</span>
          )}
        </div>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'ativo',
      key: 'ativo',
      render: (ativo: boolean) => (
        <Tag color={ativo ? 'green' : 'red'}>
          {ativo ? 'Ativo' : 'Inativo'}
        </Tag>
      ),
    },
    {
      title: 'Ações',
      key: 'acoes',
      render: (record: Procedimento) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => onEdit(record)}
            title="Editar"
          />
          <Popconfirm
            title="Tem certeza que deseja excluir este procedimento?"
            onConfirm={() => handleDelete(record.id)}
            okText="Sim"
            cancelText="Não"
          >
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              title="Excluir"
            />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <Card
      title="Procedimentos"
      extra={
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={onNew}
        >
          Novo Procedimento
        </Button>
      }
    >
      <Table
        columns={columns}
        dataSource={procedimentos}
        rowKey="id"
        loading={loading}
        pagination={{
          ...pagination,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) =>
            `${range[0]}-${range[1]} de ${total} procedimentos`,
        }}
        onChange={handleTableChange}
        scroll={{ x: 800 }}
      />
    </Card>
  );
};

export default ProcedimentoTable; 