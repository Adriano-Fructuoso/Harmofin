import React, { useState, useEffect } from 'react';
import { Layout, Modal, message, Card, Row, Col, Statistic } from 'antd';
import { UserOutlined, CalendarOutlined, DollarOutlined } from '@ant-design/icons';
import AtendimentoTable from '../components/AtendimentoTable';
import AtendimentoForm from '../components/AtendimentoForm';
import { Atendimento, AtendimentoCreate, AtendimentoUpdate } from '../types/atendimento';
import { atendimentosApi } from '../services/api';
import dayjs from 'dayjs';

const { Content } = Layout;

const Atendimentos: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('Novo Atendimento');
  const [editingAtendimento, setEditingAtendimento] = useState<Atendimento | null>(null);
  const [loading, setLoading] = useState(false);
  const [estatisticas, setEstatisticas] = useState({
    total_atendimentos: 0,
    atendimentos_hoje: 0,
    atendimentos_mes: 0,
    valor_total_mes: 0
  });
  const [refresh, setRefresh] = useState(0);

  const carregarEstatisticas = async () => {
    try {
      console.log('Carregando estatísticas...');
      const response = await atendimentosApi.estatisticas();
      console.log('Estatísticas recebidas:', response.data);
      setEstatisticas(response.data);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleNewAtendimento = () => {
    setEditingAtendimento(null);
    setModalTitle('Novo Atendimento');
    setModalVisible(true);
  };

  const handleEditAtendimento = (atendimento: Atendimento) => {
    console.log('handleEditAtendimento chamado com:', atendimento);
    setEditingAtendimento(atendimento);
    setModalTitle('Editar Atendimento');
    setModalVisible(true);
  };

  const handleViewAtendimento = (atendimento: Atendimento) => {
    Modal.info({
      title: `Atendimento #${atendimento.id}`,
      width: 600,
      content: (
        <div>
          <p><strong>Cliente:</strong> {atendimento.cliente.nome}</p>
          <p><strong>Telefone:</strong> {atendimento.cliente.telefone}</p>
          <p><strong>Procedimentos:</strong></p>
          <ul>
            {atendimento.procedimentos && atendimento.procedimentos.length > 0 ? (
              atendimento.procedimentos.map((proc, idx) => (
                <li key={proc.id || idx}>
                  {proc?.procedimento?.nome || 'Procedimento não encontrado'}
                  {!proc?.procedimento?.nome && (
                    <span style={{ color: 'red', marginLeft: 8 }}>⚠️ Procedimento faltando</span>
                  )}
                </li>
              ))
            ) : (
              <li>
                {atendimento.procedimento?.nome || 'Procedimento não encontrado'}
                {!atendimento.procedimento?.nome && (
                  <span style={{ color: 'red', marginLeft: 8 }}>⚠️ Procedimento faltando</span>
                )}
              </li>
            )}
          </ul>
          <p><strong>Data/Hora:</strong> {new Date(atendimento.data_hora).toLocaleString()}</p>
          <p><strong>Valor:</strong> R$ {atendimento.valor_cobrado.toFixed(2)}</p>
          <p><strong>Status:</strong> {atendimento.status}</p>
          {atendimento.observacoes && (
            <p><strong>Observações:</strong> {atendimento.observacoes}</p>
          )}
          {atendimento.materiais_utilizados.length > 0 && (
            <div>
              <p><strong>Materiais Utilizados:</strong></p>
              <ul>
                {atendimento.materiais_utilizados.map((material, index) => (
                  <li key={index}>
                    {material.material?.nome || 'Material não encontrado'} - {material.quantidade_utilizada} {material.material?.unidade || 'un'}
                    (R$ {material.valor_unitario_momento?.toFixed(2) || '0.00'} cada)
                    {!material.material?.nome && (
                      <span style={{ color: 'red', marginLeft: 8 }}>⚠️ Material faltando</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )
    });
  };

  const handleSubmit = async (values: AtendimentoCreate) => {
    console.log('Atendimentos - handleSubmit chamado com valores:', values);
    console.log('editingAtendimento:', editingAtendimento);
    
    try {
      setLoading(true);
      
      if (editingAtendimento) {
        console.log('Atualizando atendimento existente...');
        // Atualizar atendimento existente
        const updateData: AtendimentoUpdate = {
          cliente_id: values.cliente_id,
          procedimento_id: values.procedimento_id,
          data_hora: values.data_hora,
          valor_cobrado: values.valor_cobrado,
          observacoes: values.observacoes,
          status: values.status
        };
        
        console.log('Dados de atualização:', updateData);
        await atendimentosApi.atualizar(editingAtendimento.id, updateData);
        message.success('Atendimento atualizado com sucesso!');
      } else {
        console.log('Criando novo atendimento...');
        // Criar novo atendimento
        await atendimentosApi.criar(values);
        message.success('Atendimento criado com sucesso!');
      }
      
      setModalVisible(false);
      carregarEstatisticas();
      setRefresh(r => r + 1);
    } catch (error: any) {
      console.error('Erro no handleSubmit:', error);
      message.error(error.response?.data?.detail || 'Erro ao salvar atendimento');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAtendimento = async (id: number) => {
    try {
      console.log('Excluindo atendimento:', id);
      await atendimentosApi.remover(id);
      message.success('Atendimento removido com sucesso!');
      console.log('Atendimento excluído, carregando estatísticas...');
      await carregarEstatisticas(); // Aguardar a conclusão
      console.log('Estatísticas atualizadas, incrementando refresh...');
      setRefresh(r => r + 1);
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao remover atendimento');
    }
  };

  // Carregar estatísticas ao montar o componente
  useEffect(() => {
    carregarEstatisticas();
  }, []);

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        {/* Estatísticas */}
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Total de Atendimentos"
                value={estatisticas.total_atendimentos}
                prefix={<UserOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Atendimentos Hoje"
                value={estatisticas.atendimentos_hoje}
                prefix={<CalendarOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Atendimentos no Mês"
                value={estatisticas.atendimentos_mes}
                prefix={<CalendarOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Valor Total do Mês"
                value={estatisticas.valor_total_mes}
                prefix={<DollarOutlined />}
                precision={2}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
        </Row>

        {/* Tabela de Atendimentos */}
        <AtendimentoTable
          onNew={handleNewAtendimento}
          onEdit={handleEditAtendimento}
          onView={handleViewAtendimento}
          onDelete={handleDeleteAtendimento}
          refresh={refresh}
        />

        {/* Modal do Formulário */}
        <Modal
          title={modalTitle}
          open={modalVisible}
          onCancel={() => setModalVisible(false)}
          footer={null}
          width={800}
          destroyOnHidden
        >
          <AtendimentoForm
            onSubmit={handleSubmit}
            loading={loading}
            initialValues={editingAtendimento ? {
              cliente_id: editingAtendimento.cliente_id,
              procedimento_id: editingAtendimento.procedimento_id,
              data_hora: dayjs(editingAtendimento.data_hora),
              valor_cobrado: editingAtendimento.valor_cobrado,
              observacoes: editingAtendimento.observacoes,
              status: editingAtendimento.status,
              materiais_utilizados: editingAtendimento.materiais_utilizados.map(m => ({
                material_id: m.material_id,
                quantidade_utilizada: m.quantidade_utilizada,
                valor_unitario_momento: m.valor_unitario_momento
              })),
              procedimentos: editingAtendimento.procedimentos && editingAtendimento.procedimentos.length > 0
                ? editingAtendimento.procedimentos.map(p => ({ 
                    procedimento_id: p.procedimento_id, 
                    valor_cobrado: p.valor_cobrado, 
                    observacoes: p.observacoes 
                  }))
                : [{ 
                    procedimento_id: editingAtendimento.procedimento_id, 
                    valor_cobrado: editingAtendimento.valor_cobrado 
                  }]
            } : undefined}
          />
        </Modal>
      </Content>
    </Layout>
  );
};

export default Atendimentos; 