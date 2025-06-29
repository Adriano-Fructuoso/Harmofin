import React, { useState, useEffect } from 'react';
import { Layout, Button, Modal, message, Card, Row, Col, Statistic, Alert } from 'antd';
import { 
  InboxOutlined, DollarOutlined, ExclamationCircleOutlined, 
  WarningOutlined, CheckCircleOutlined 
} from '@ant-design/icons';
import MaterialTable from '../components/MaterialTable';
import MaterialForm from '../components/MaterialForm';
import { Material, MaterialCreate, MaterialUpdate } from '../types/material';
import { materiaisApi } from '../services/api';

const { Content } = Layout;

const Materiais: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalTitle, setModalTitle] = useState('Novo Material');
  const [editingMaterial, setEditingMaterial] = useState<Material | null>(null);
  const [loading, setLoading] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [estatisticas, setEstatisticas] = useState({
    total_materiais: 0,
    materiais_ativos: 0,
    materiais_estoque_baixo: 0,
    valor_total_estoque: 0
  });
  const [estoqueBaixo, setEstoqueBaixo] = useState<Material[]>([]);
  const [mostrarAlertaEstoque, setMostrarAlertaEstoque] = useState(true);

  const carregarEstatisticas = async () => {
    try {
      const [ativosRes, estoqueBaixoRes] = await Promise.all([
        materiaisApi.listar({ ativo: true }),
        materiaisApi.estoqueBaixo()
      ]);

      const materiaisAtivos = ativosRes.data.materiais;
      const materiaisEstoqueBaixo = estoqueBaixoRes.data.materiais;

      console.log('Materiais com estoque baixo:', materiaisEstoqueBaixo.map(m => ({
        id: m.id,
        nome: m.nome,
        quantidade: m.quantidade_disponivel,
        minimo: m.estoque_minimo
      })));

      // Função para normalizar nome (igual à da tabela)
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

      // Agrupar materiais com estoque baixo (igual à tabela)
      const grupos: { [nomeNormalizado: string]: Material[] } = {};
      materiaisEstoqueBaixo.forEach(mat => {
        const chave = normalizarNome(mat.nome);
        if (!grupos[chave]) grupos[chave] = [];
        grupos[chave].push(mat);
      });

      // Para cada grupo, somar quantidade e verificar se ainda está com estoque baixo
      const materiaisEstoqueBaixoAgrupados = Object.values(grupos).map(grupo => {
        if (grupo.length === 1) {
          return grupo[0];
        } else {
          const representante = { ...grupo[0] };
          representante.quantidade_disponivel = grupo.reduce((soma, m) => soma + m.quantidade_disponivel, 0);
          return representante;
        }
      }).filter(material => material.quantidade_disponivel <= material.estoque_minimo);

      console.log('Materiais com estoque baixo após agrupamento:', materiaisEstoqueBaixoAgrupados.map(m => ({
        nome: m.nome,
        quantidade: m.quantidade_disponivel,
        minimo: m.estoque_minimo
      })));

      const valorTotalEstoque = materiaisAtivos.reduce(
        (total, material) => total + (material.quantidade_disponivel * material.valor_unitario), 
        0
      );

      setEstatisticas({
        total_materiais: ativosRes.data.total,
        materiais_ativos: materiaisAtivos.length,
        materiais_estoque_baixo: materiaisEstoqueBaixoAgrupados.length,
        valor_total_estoque: valorTotalEstoque
      });

      setEstoqueBaixo(materiaisEstoqueBaixoAgrupados);
      
      // Se não há mais materiais com estoque baixo, esconder o alerta
      if (materiaisEstoqueBaixoAgrupados.length === 0) {
        setMostrarAlertaEstoque(false);
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleNewMaterial = () => {
    setEditingMaterial(null);
    setModalTitle('Novo Material');
    setModalVisible(true);
  };

  const handleEditMaterial = (material: Material) => {
    setEditingMaterial(material);
    setModalTitle('Editar Material');
    setModalVisible(true);
  };

  const handleSubmit = async (values: MaterialCreate | MaterialUpdate) => {
    try {
      setLoading(true);
      
      if (editingMaterial) {
        // Atualizar material existente
        await materiaisApi.atualizar(editingMaterial.id, values as MaterialUpdate);
        message.success('Material atualizado com sucesso!');
      } else {
        // Criar novo material
        await materiaisApi.criar(values as MaterialCreate);
        message.success('Material criado com sucesso!');
      }
      
      setModalVisible(false);
      setRefresh(r => r + 1);
      carregarEstatisticas();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao salvar material');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMaterial = async (id: number) => {
    try {
      await materiaisApi.remover(id);
      message.success('Material removido com sucesso!');
      setRefresh(r => r + 1);
      carregarEstatisticas();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Erro ao remover material');
    }
  };

  // Carregar estatísticas ao montar o componente
  useEffect(() => {
    carregarEstatisticas();
  }, []);

  return (
    <Layout style={{ padding: '24px' }}>
      <Content>
        {/* Alertas de Estoque Baixo */}
        {mostrarAlertaEstoque && estoqueBaixo.length > 0 && (
          <Alert
            message={`${estoqueBaixo.length} material(is) com estoque baixo`}
            description={
              <div>
                <p>Os seguintes materiais estão com estoque crítico:</p>
                <ul>
                  {estoqueBaixo.slice(0, 3).map(material => (
                    <li key={material.id}>
                      <strong>{material.nome}</strong> - {material.quantidade_disponivel} {material.unidade} 
                      (mín: {material.estoque_minimo} {material.unidade})
                    </li>
                  ))}
                  {estoqueBaixo.length > 3 && (
                    <li>... e mais {estoqueBaixo.length - 3} material(is)</li>
                  )}
                </ul>
              </div>
            }
            type="warning"
            showIcon
            icon={<ExclamationCircleOutlined />}
            style={{ marginBottom: 24 }}
            action={
              <Button size="small" onClick={() => setMostrarAlertaEstoque(false)}>
                Fechar
              </Button>
            }
          />
        )}

        {/* Estatísticas */}
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Total de Materiais"
                value={estatisticas.total_materiais}
                prefix={<InboxOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Materiais Ativos"
                value={estatisticas.materiais_ativos}
                prefix={<CheckCircleOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Estoque Baixo"
                value={estatisticas.materiais_estoque_baixo}
                prefix={<WarningOutlined />}
                valueStyle={{ color: estatisticas.materiais_estoque_baixo > 0 ? '#cf1322' : '#3f8600' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Valor Total do Estoque"
                value={estatisticas.valor_total_estoque}
                prefix={<DollarOutlined />}
                precision={2}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
        </Row>

        {/* Tabela de Materiais */}
        <MaterialTable
          onNew={handleNewMaterial}
          onEdit={handleEditMaterial}
          onDelete={handleDeleteMaterial}
          refresh={refresh}
          onEstoqueAjustado={carregarEstatisticas}
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
          <MaterialForm
            onSave={handleSubmit}
            material={editingMaterial || undefined}
          />
        </Modal>
      </Content>
    </Layout>
  );
};

export default Materiais; 