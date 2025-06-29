import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Popconfirm, Input, message } from 'antd';
import { EditOutlined, DeleteOutlined, SearchOutlined, PlusOutlined } from '@ant-design/icons';
import { Cliente } from '../types/atendimento';
import { clientesApi } from '../services/api';

interface ClienteTableProps {
  onNew: () => void;
  onEdit: (cliente: Cliente) => void;
  onView: (cliente: Cliente) => void;
  refreshTrigger?: number; // Prop para forçar refresh
}

const ClienteTable: React.FC<ClienteTableProps> = ({
  onNew,
  onEdit,
  onView,
  refreshTrigger = 0,
}) => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const carregarClientes = async () => {
    try {
      setLoading(true);
      const response = await clientesApi.listar();
      setClientes(response.data.clientes);
    } catch (error) {
      message.error('Erro ao carregar clientes');
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      carregarClientes();
      return;
    }

    try {
      setLoading(true);
      const response = await clientesApi.buscar(searchTerm);
      setClientes(response.data.clientes);
    } catch (error) {
      message.error('Erro na busca');
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await clientesApi.remover(id);
      message.success('Cliente removido com sucesso!');
      carregarClientes();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao remover cliente');
    }
  };

  // Carregar clientes quando o componente montar
  useEffect(() => {
    carregarClientes();
  }, []);

  // Recarregar quando refreshTrigger mudar
  useEffect(() => {
    if (refreshTrigger > 0) {
      carregarClientes();
    }
  }, [refreshTrigger]);

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Nome',
      dataIndex: 'nome',
      key: 'nome',
      sorter: (a: Cliente, b: Cliente) => a.nome.localeCompare(b.nome),
    },
    {
      title: 'Telefone',
      dataIndex: 'telefone',
      key: 'telefone',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      render: (email: string) => email || '-',
    },
    {
      title: 'Observação',
      dataIndex: 'observacao',
      key: 'observacao',
      render: (observacao: string) => observacao || '-',
      ellipsis: true,
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 150,
      render: (_: any, record: Cliente) => (
        <Space size="small">
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => onEdit(record)}
            title="Editar"
          />
          <Button
            type="text"
            onClick={() => onView(record)}
            title="Visualizar"
          >
            Ver
          </Button>
          <Popconfirm
            title="Tem certeza que deseja remover este cliente?"
            onConfirm={() => handleDelete(record.id)}
            okText="Sim"
            cancelText="Não"
          >
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              title="Remover"
            />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', gap: 8, justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', gap: 8 }}>
          <Input
            placeholder="Buscar por nome ou telefone..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onPressEnter={handleSearch}
            style={{ width: 300 }}
            prefix={<SearchOutlined />}
          />
          <Button type="primary" onClick={handleSearch}>
            Buscar
          </Button>
          <Button onClick={carregarClientes}>Limpar</Button>
        </div>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={onNew}
        >
          Novo Cliente
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={clientes}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) =>
            `${range[0]}-${range[1]} de ${total} clientes`,
        }}
      />
    </div>
  );
};

export default ClienteTable; 