import React, { useState, useEffect } from 'react';
import { Layout, Button, Modal, message, Card, Row, Col, Statistic } from 'antd';
import { PlusOutlined, MedicineBoxOutlined, DollarOutlined, CheckCircleOutlined } from '@ant-design/icons';
import ProcedimentoTable from '../components/ProcedimentoTable';
import ProcedimentoForm from '../components/ProcedimentoForm';
import { Procedimento, ProcedimentoCreate, ProcedimentoUpdate } from '../types/procedimento';
import { procedimentosApi } from '../services/api';

const { Content } = Layout;

const Procedimentos: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('Novo Procedimento');
  const [editingProcedimento, setEditingProcedimento] = useState<Procedimento | null>(null);
  const [loading, setLoading] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [estatisticas, setEstatisticas] = useState({
    total_procedimentos: 0,
    procedimentos_ativos: 0,
    valor_medio: 0
  });

  const carregarEstatisticas = async () => {
    try {
      const [ativosRes, todosRes] = await Promise.all([
        procedimentosApi.listar({ ativo: true }),
        procedimentosApi.listar()
      ]);

      const procedimentosAtivos = ativosRes.data.procedimentos;
      const todosProcedimentos = todosRes.data.procedimentos;

      const valorMedio = procedimentosAtivos.length > 0 
        ? procedimentosAtivos.reduce((total, proc) => total + proc.valor_padrao, 0) / procedimentosAtivos.length
        : 0;

      setEstatisticas({
        total_procedimentos: todosRes.data.total,
        procedimentos_ativos: procedimentosAtivos.length,
        valor_medio: valorMedio
      });
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleNewProcedimento = () => {
    setEditingProcedimento(null);
    setModalTitle('Novo Procedimento');
    setModalVisible(true);
  };

  const handleEditProcedimento = (procedimento: Procedimento) => {
    setEditingProcedimento(procedimento);
    setModalTitle('Editar Procedimento');
    setModalVisible(true);
  };

  const handleSubmit = async (values: ProcedimentoCreate) => {
    try {
      setLoading(true);
      console.log('🔍 Procedimentos - handleSubmit chamado com valores:', values);
      
      if (editingProcedimento) {
        // Atualizar procedimento existente
        console.log('📝 Atualizando procedimento ID:', editingProcedimento.id);
        await procedimentosApi.atualizar(editingProcedimento.id, values as ProcedimentoUpdate);
        message.success('Procedimento atualizado com sucesso!');
      } else {
        // Criar novo procedimento
        console.log('🆕 Criando novo procedimento');
        await procedimentosApi.criar(values);
        message.success('Procedimento criado com sucesso!');
      }
      
      setModalVisible(false);
      setRefresh(r => r + 1);
      carregarEstatisticas();
    } catch (error: any) {
      console.error('❌ Erro ao salvar procedimento:', error);
      console.error('❌ Detalhes do erro:', error.response?.data);
      message.error(error.response?.data?.detail || 'Erro ao salvar procedimento');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProcedimento = async (id: number) => {
    try {
      await procedimentosApi.remover(id);
      message.success('Procedimento removido com sucesso!');
      setRefresh(r => r + 1);
      carregarEstatisticas();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao remover procedimento');
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
          <Col span={8}>
            <Card>
              <Statistic
                title="Total de Procedimentos"
                value={estatisticas.total_procedimentos}
                prefix={<MedicineBoxOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Procedimentos Ativos"
                value={estatisticas.procedimentos_ativos}
                prefix={<CheckCircleOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Valor Médio"
                value={estatisticas.valor_medio}
                prefix={<DollarOutlined />}
                precision={2}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
        </Row>

        {/* Tabela de Procedimentos */}
        <ProcedimentoTable
          onNew={handleNewProcedimento}
          onEdit={handleEditProcedimento}
          onDelete={handleDeleteProcedimento}
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
          <ProcedimentoForm
            onSubmit={handleSubmit}
            loading={loading}
            initialValues={editingProcedimento ? {
              nome: editingProcedimento.nome,
              descricao: editingProcedimento.descricao,
              valor_padrao: editingProcedimento.valor_padrao,
              ativo: editingProcedimento.ativo,
              materiais_padrao: editingProcedimento.materiais_padrao?.map(mp => ({
                material_id: mp.material_id,
                quantidade_padrao: mp.quantidade_padrao
              })) || []
            } : undefined}
          />
        </Modal>
      </Content>
    </Layout>
  );
};

export default Procedimentos; 