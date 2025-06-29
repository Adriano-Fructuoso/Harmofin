import React, { useState } from 'react';
import { Layout, Modal, message, Card, Row, Col, Statistic } from 'antd';
import { UserOutlined, PhoneOutlined, MailOutlined } from '@ant-design/icons';
import ClienteTable from '../components/ClienteTable';
import ClienteForm from '../components/ClienteForm';
import { Cliente, ClienteCreate, ClienteUpdate } from '../types/atendimento';
import { clientesApi } from '../services/api';

const { Content } = Layout;

const Clientes: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('Novo Cliente');
  const [editingCliente, setEditingCliente] = useState<Cliente | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [estatisticas, setEstatisticas] = useState({
    total_clientes: 0,
    com_email: 0,
    com_observacao: 0
  });

  const carregarEstatisticas = async () => {
    try {
      const response = await clientesApi.listar();
      const clientes = response.data.clientes;
      setEstatisticas({
        total_clientes: clientes.length,
        com_email: clientes.filter(c => c.email).length,
        com_observacao: clientes.filter(c => c.observacao).length
      });
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleNewCliente = () => {
    setEditingCliente(null);
    setModalTitle('Novo Cliente');
    setModalVisible(true);
  };

  const handleEditCliente = (cliente: Cliente) => {
    setEditingCliente(cliente);
    setModalTitle('Editar Cliente');
    setModalVisible(true);
  };

  const handleViewCliente = (cliente: Cliente) => {
    Modal.info({
      title: `Cliente: ${cliente.nome}`,
      width: 500,
      content: (
        <div>
          <p><strong>ID:</strong> {cliente.id}</p>
          <p><strong>Nome:</strong> {cliente.nome}</p>
          <p><strong>Telefone:</strong> {cliente.telefone}</p>
          {cliente.email && <p><strong>Email:</strong> {cliente.email}</p>}
          {cliente.observacao && <p><strong>Observação:</strong> {cliente.observacao}</p>}
          <p><strong>Data de Cadastro:</strong> {new Date(cliente.data_cadastro).toLocaleDateString()}</p>
        </div>
      )
    });
  };

  const handleSubmit = async (values: ClienteCreate) => {
    try {
      setLoading(true);
      
      if (editingCliente) {
        // Atualizar cliente existente
        const updateData: ClienteUpdate = {
          nome: values.nome,
          telefone: values.telefone,
          email: values.email,
          observacao: values.observacao
        };
        
        await clientesApi.atualizar(editingCliente.id, updateData);
        message.success('Cliente atualizado com sucesso!');
      } else {
        // Criar novo cliente
        await clientesApi.criar(values);
        message.success('Cliente criado com sucesso!');
      }
      
      setModalVisible(false);
      carregarEstatisticas();
      // Forçar recarregamento da lista
      setRefreshTrigger(prev => prev + 1);
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao salvar cliente');
    } finally {
      setLoading(false);
    }
  };

  // Carregar estatísticas ao montar o componente
  React.useEffect(() => {
    carregarEstatisticas();
  }, []);

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        {/* Estatísticas */}
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={8}>
            <Card>
              <Statistic
                title="Total de Clientes"
                value={estatisticas.total_clientes}
                prefix={<UserOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Com Email"
                value={estatisticas.com_email}
                prefix={<MailOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Com Observação"
                value={estatisticas.com_observacao}
                prefix={<PhoneOutlined />}
              />
            </Card>
          </Col>
        </Row>

        {/* Tabela de Clientes */}
        <ClienteTable
          onNew={handleNewCliente}
          onEdit={handleEditCliente}
          onView={handleViewCliente}
          refreshTrigger={refreshTrigger}
        />

        {/* Modal do Formulário */}
        <Modal
          title={modalTitle}
          open={modalVisible}
          onCancel={() => setModalVisible(false)}
          footer={null}
          width={600}
          destroyOnHidden
        >
          <ClienteForm
            onSubmit={handleSubmit}
            loading={loading}
            initialValues={editingCliente ? {
              nome: editingCliente.nome,
              telefone: editingCliente.telefone,
              email: editingCliente.email,
              observacao: editingCliente.observacao
            } : undefined}
          />
        </Modal>
      </Content>
    </Layout>
  );
};

export default Clientes; 