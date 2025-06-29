import React, { useState, useEffect } from 'react';
import { Table, Card, Button, Space, Tag, Modal, message, DatePicker, Select } from 'antd';
import { EditOutlined, DeleteOutlined, EyeOutlined, PlusOutlined } from '@ant-design/icons';
import { Atendimento, Cliente, Procedimento } from '../types/atendimento';
import { atendimentosApi, clientesApi, procedimentosApi } from '../services/api';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;
const { Option } = Select;

interface AtendimentoTableProps {
  onEdit?: (atendimento: Atendimento) => void;
  onView?: (atendimento: Atendimento) => void;
  onDelete?: (id: number) => void;
  onNew?: () => void;
  refresh?: number;
}

const AtendimentoTable: React.FC<AtendimentoTableProps> = ({
  onEdit,
  onView,
  onDelete,
  onNew,
  refresh
}) => {
  const [atendimentos, setAtendimentos] = useState<Atendimento[]>([]);
  const [loading, setLoading] = useState(false);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [procedimentos, setProcedimentos] = useState<Procedimento[]>([]);
  const [filtros, setFiltros] = useState({
    cliente_id: undefined as number | undefined,
    procedimento_id: undefined as number | undefined,
    data_inicio: undefined as string | undefined,
    data_fim: undefined as string | undefined,
    status: undefined as string | undefined
  });

  // Verificar se há dados faltantes
  const verificarDadosFaltantes = () => {
    const procedimentosFaltantes = atendimentos.filter(atendimento => {
      if (atendimento.procedimentos && atendimento.procedimentos.length > 0) {
        return atendimento.procedimentos.some(proc => !proc.procedimento?.nome);
      }
      return !atendimento.procedimento?.nome;
    });

    const materiaisFaltantes = atendimentos.filter(atendimento => 
      atendimento.materiais_utilizados?.some(material => !material.material?.nome)
    );

    return {
      procedimentos: procedimentosFaltantes.length,
      materiais: materiaisFaltantes.length
    };
  };

  const dadosFaltantes = verificarDadosFaltantes();

  useEffect(() => {
    carregarDados();
  }, [filtros, refresh]);

  const carregarDados = async () => {
    try {
      setLoading(true);
      const [atendimentosRes, clientesRes, procedimentosRes] = await Promise.all([
        atendimentosApi.listar(filtros),
        clientesApi.listar(),
        procedimentosApi.listar()
      ]);

      setAtendimentos(atendimentosRes.data.atendimentos);
      setClientes(clientesRes.data.clientes);
      setProcedimentos(procedimentosRes.data.procedimentos);
    } catch (error) {
      message.error('Erro ao carregar atendimentos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: 'Confirmar exclusão',
      content: 'Tem certeza que deseja excluir este atendimento?',
      okText: 'Sim',
      cancelText: 'Não',
      onOk: async () => {
        try {
          if (onDelete) {
            await onDelete(id);
          } else {
            await atendimentosApi.remover(id);
            message.success('Atendimento removido com sucesso');
            carregarDados(); // Atualização imediata
          }
        } catch (error) {
          message.error('Erro ao remover atendimento');
        }
      }
    });
  };

  const handleDateRangeChange = (dates: any) => {
    setFiltros(prev => ({
      ...prev,
      data_inicio: dates?.[0]?.toISOString(),
      data_fim: dates?.[1]?.toISOString()
    }));
  };

  const handleResetFiltros = () => {
    setFiltros({
      cliente_id: undefined,
      procedimento_id: undefined,
      data_inicio: undefined,
      data_fim: undefined,
      status: undefined
    });
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Cliente',
      dataIndex: 'cliente',
      key: 'cliente',
      render: (cliente: Cliente) => (
        <div>
          <div><strong>{cliente.nome}</strong></div>
          <div style={{ fontSize: '12px', color: '#666' }}>{cliente.telefone}</div>
        </div>
      ),
    },
    {
      title: 'Procedimentos',
      dataIndex: 'procedimentos',
      key: 'procedimentos',
      render: (procedimentos: any[], record: Atendimento) => {
        // Se não há procedimentos múltiplos, mostrar o procedimento principal
        if (!procedimentos || procedimentos.length === 0) {
          return (
            <div>
              <div><strong>{record.procedimento?.nome || 'Procedimento não encontrado'}</strong></div>
              {!record.procedimento?.nome && (
                <Tag color="red" style={{ fontSize: '10px', marginTop: 2 }}>
                  ⚠️ Procedimento faltando
                </Tag>
              )}
            </div>
          );
        }
        // Mostrar lista de nomes dos procedimentos
        return (
          <div>
            {procedimentos.map((proc, index) => {
              const nomeProcedimento = proc?.procedimento?.nome;
              const temProcedimento = !!nomeProcedimento;
              
              return (
                <div key={proc.id || index} style={{ marginBottom: index < procedimentos.length - 1 ? 4 : 0 }}>
                  <span style={{ fontSize: '13px' }}>
                    {nomeProcedimento || 'Procedimento não encontrado'}
                  </span>
                  {!temProcedimento && (
                    <Tag color="red" style={{ fontSize: '10px', marginLeft: 4 }}>
                      ⚠️
                    </Tag>
                  )}
                </div>
              );
            })}
          </div>
        );
      },
    },
    {
      title: 'Data/Hora',
      dataIndex: 'data_hora',
      key: 'data_hora',
      render: (data: string) => dayjs(data).format('DD/MM/YYYY HH:mm'),
      sorter: (a: Atendimento, b: Atendimento) => 
        dayjs(a.data_hora).unix() - dayjs(b.data_hora).unix(),
    },
    {
      title: 'Valor',
      dataIndex: 'valor_cobrado',
      key: 'valor_cobrado',
      render: (valor: number) => `R$ ${valor.toFixed(2)}`,
      sorter: (a: Atendimento, b: Atendimento) => a.valor_cobrado - b.valor_cobrado,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const color = status === 'realizado' ? 'green' : 
                     status === 'cancelado' ? 'red' : 'orange';
        return <Tag color={color}>{status.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Materiais',
      dataIndex: 'materiais_utilizados',
      key: 'materiais_utilizados',
      render: (materiais: any[]) => (
        <div>
          {materiais && materiais.length > 0 ? (
            <Tag color="blue">{materiais.length} material(is)</Tag>
          ) : (
            <Tag color="default">Nenhum</Tag>
          )}
        </div>
      ),
    },
    {
      title: 'Ações',
      key: 'actions',
      width: 150,
      render: (_: any, record: Atendimento) => (
        <Space>
          {onView && (
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => onView(record)}
              title="Visualizar"
            />
          )}
          {onEdit && (
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => onEdit(record)}
              title="Editar"
            />
          )}
          {onDelete && (
            <Button
              type="text"
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
    <Card title="Atendimentos" extra={
      onNew && (
        <Button type="primary" icon={<PlusOutlined />} onClick={onNew}>
          Novo Atendimento
        </Button>
      )
    }>
      {/* Alerta de dados faltantes */}
      {(dadosFaltantes.procedimentos > 0 || dadosFaltantes.materiais > 0) && (
        <div style={{ marginBottom: 16 }}>
          <Card size="small" style={{ backgroundColor: '#fff2e8', borderColor: '#ffbb96' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: '#d46b08', fontSize: '16px' }}>⚠️</span>
              <span style={{ color: '#d46b08', fontWeight: 500 }}>
                Atenção: Dados faltantes detectados
              </span>
            </div>
            <div style={{ marginTop: 8, fontSize: '13px', color: '#d46b08' }}>
              {dadosFaltantes.procedimentos > 0 && (
                <div>• {dadosFaltantes.procedimentos} atendimento(s) com procedimento(s) faltando</div>
              )}
              {dadosFaltantes.materiais > 0 && (
                <div>• {dadosFaltantes.materiais} atendimento(s) com material(is) faltando</div>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Filtros */}
      <div style={{ marginBottom: 16 }}>
        <Space wrap>
          <Select
            placeholder="Filtrar por cliente"
            allowClear
            style={{ width: 200 }}
            onChange={(value) => setFiltros(prev => ({ ...prev, cliente_id: value }))}
          >
            {clientes.map(cliente => (
              <Option key={cliente.id} value={cliente.id}>
                {cliente.nome}
              </Option>
            ))}
          </Select>

          <Select
            placeholder="Filtrar por procedimento"
            allowClear
            style={{ width: 200 }}
            onChange={(value) => setFiltros(prev => ({ ...prev, procedimento_id: value }))}
          >
            {procedimentos.map(procedimento => (
              <Option key={procedimento.id} value={procedimento.id}>
                {procedimento.nome}
              </Option>
            ))}
          </Select>

          <RangePicker
            placeholder={['Data início', 'Data fim']}
            onChange={handleDateRangeChange}
            format="DD/MM/YYYY"
          />

          <Select
            placeholder="Status"
            allowClear
            style={{ width: 120 }}
            onChange={(value) => setFiltros(prev => ({ ...prev, status: value }))}
          >
            <Option value="realizado">Realizado</Option>
            <Option value="cancelado">Cancelado</Option>
            <Option value="reagendado">Reagendado</Option>
          </Select>

          <Button onClick={handleResetFiltros}>
            Limpar Filtros
          </Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={atendimentos}
        rowKey="id"
        loading={loading}
        pagination={{
          total: atendimentos.length,
          pageSize: 10,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => 
            `${range[0]}-${range[1]} de ${total} atendimentos`,
        }}
      />
    </Card>
  );
};

export default AtendimentoTable; 