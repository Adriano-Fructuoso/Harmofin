import React, { useState, useEffect } from 'react';
import { Form, Input, Select, DatePicker, InputNumber, Button, Card, Space, Divider, message } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { AtendimentoCreate, Cliente, Procedimento, Material } from '../types/atendimento';
import { clientesApi, procedimentosApi, materiaisApi } from '../services/api';
import MaterialSelector from './MaterialSelector';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';

const { TextArea } = Input;
const { Option } = Select;

interface AtendimentoFormProps {
  onSubmit: (values: AtendimentoCreate) => void;
  loading?: boolean;
  initialValues?: Partial<Omit<AtendimentoCreate, 'data_hora'>> & { data_hora?: string | Dayjs };
}

const AtendimentoForm: React.FC<AtendimentoFormProps> = ({ 
  onSubmit, 
  loading = false, 
  initialValues 
}) => {
  const [form] = Form.useForm();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [procedimentos, setProcedimentos] = useState<Procedimento[]>([]);
  const [materiais, setMateriais] = useState<Material[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  // Aplicar initialValues quando eles mudarem (para edição)
  useEffect(() => {
    console.log('AtendimentoForm - useEffect initialValues:', initialValues);
    if (initialValues) {
      const formValues = {
        data_hora: initialValues.data_hora ? dayjs(initialValues.data_hora) : dayjs(),
        status: initialValues.status || 'realizado',
        materiais_utilizados: initialValues.materiais_utilizados || [],
        procedimentos: initialValues.procedimentos && initialValues.procedimentos.length > 0 
          ? initialValues.procedimentos 
          : [{}],
        ...initialValues
      };
      console.log('Aplicando valores ao formulário:', formValues);
      form.setFieldsValue(formValues);
    }
  }, [initialValues, form]);

  const carregarDados = async () => {
    try {
      setLoadingData(true);
      const [clientesRes, procedimentosRes, materiaisRes] = await Promise.all([
        clientesApi.listar(),
        procedimentosApi.listar({ ativo: true }),
        materiaisApi.listar({ ativo: true })
      ]);

      setClientes(clientesRes.data.clientes);
      setProcedimentos(procedimentosRes.data.procedimentos);
      setMateriais(materiaisRes.data.materiais);
    } catch (error) {
      message.error('Erro ao carregar dados');
    } finally {
      setLoadingData(false);
    }
  };

  const handleSubmit = (values: any) => {
    console.log('AtendimentoForm - handleSubmit chamado com valores:', values);
    
    // Processar múltiplos procedimentos
    const procedimentosSelecionados = values.procedimentos || [];
    const procedimentoIds = procedimentosSelecionados.map((p: any) => p.procedimento_id).filter(Boolean);
    
    console.log('Procedimentos selecionados:', procedimentosSelecionados);
    console.log('IDs dos procedimentos:', procedimentoIds);
    
    // Validar se pelo menos um procedimento foi selecionado
    if (procedimentoIds.length === 0) {
      message.error('Selecione pelo menos um procedimento');
      return;
    }
    
    // Calcular valor total
    const valorTotal = procedimentosSelecionados.reduce((total: number, p: any) => {
      if (p.procedimento_id) {
        const proc = procedimentos.find(proc => proc.id === p.procedimento_id);
        return total + (proc?.valor_padrao || 0);
      }
      return total;
    }, 0);
    
    const atendimentoData: AtendimentoCreate = {
      cliente_id: values.cliente_id,
      procedimento_id: procedimentoIds[0],
      data_hora: values.data_hora.toISOString(),
      valor_cobrado: valorTotal,
      observacoes: values.observacoes,
      status: values.status,
      procedimentos: procedimentosSelecionados.map((p: any) => ({
        procedimento_id: p.procedimento_id,
        valor_cobrado: procedimentos.find(proc => proc.id === p.procedimento_id)?.valor_padrao || 0,
        observacoes: ''
      })),
      materiais_utilizados: values.materiais_utilizados || []
    };
    
    console.log('Dados do atendimento a serem enviados:', atendimentoData);
    onSubmit(atendimentoData);
  };

  const handleProcedimentoChange = async (procedimentoId: number, index?: number) => {
    const procedimento = procedimentos.find(p => p.id === procedimentoId);
    if (procedimento) {
      // Se for o primeiro procedimento, definir como valor principal
      if (index === 0 || index === undefined) {
        form.setFieldsValue({ valor_cobrado: procedimento.valor_padrao });
      }
      
      // Calcular valor total de todos os procedimentos
      const procedimentosAtuais = form.getFieldValue('procedimentos') || [];
      const valorTotal = procedimentosAtuais.reduce((total: number, p: any) => {
        if (p.procedimento_id) {
          const proc = procedimentos.find(proc => proc.id === p.procedimento_id);
          return total + (proc?.valor_padrao || 0);
        }
        return total;
      }, 0);
      
      form.setFieldsValue({ valor_cobrado: valorTotal });

      // Recarregar todos os materiais padrão baseado nos procedimentos atuais
      await recarregarMateriaisPadrao();
    }
  };

  const recarregarMateriaisPadrao = async () => {
    try {
      const procedimentosAtuais = form.getFieldValue('procedimentos') || [];
      const materiaisUtilizados: any[] = [];
      
      // Para cada procedimento, carregar seus materiais padrão
      for (const proc of procedimentosAtuais) {
        if (proc.procedimento_id) {
          const response = await procedimentosApi.materiaisPadrao(proc.procedimento_id);
          const materiaisPadrao = response.data;
          
          if (materiaisPadrao && materiaisPadrao.length > 0) {
            materiaisPadrao.forEach((mp: any) => {
              const material = materiais.find(m => m.id === mp.material_id);
              if (material) {
                // Verificar se o material já existe na lista
                const materialExistente = materiaisUtilizados.find((mu: any) => mu.material_id === mp.material_id);
                if (materialExistente) {
                  // Se já existe, somar a quantidade
                  materialExistente.quantidade_utilizada += mp.quantidade_padrao;
                } else {
                  // Se não existe, adicionar novo
                  materiaisUtilizados.push({
                    material_id: mp.material_id,
                    quantidade_utilizada: mp.quantidade_padrao,
                    valor_unitario_momento: material.valor_unitario
                  });
                }
              }
            });
          }
        }
      }
      
      // Atualizar o formulário com os materiais calculados
      form.setFieldsValue({ materiais_utilizados: materiaisUtilizados });
      
      console.log('Materiais padrão recarregados:', materiaisUtilizados);
    } catch (error) {
      console.error('Erro ao carregar materiais padrão:', error);
    }
  };

  const handleProcedimentoRemove = async (index: number) => {
    // Após remover o procedimento, recarregar materiais
    setTimeout(async () => {
      await recarregarMateriaisPadrao();
    }, 100);
  };

  const handleProcedimentoAdd = async () => {
    // Após adicionar o procedimento, recarregar materiais
    setTimeout(async () => {
      await recarregarMateriaisPadrao();
    }, 100);
  };

  const handleMaterialChange = (materialId: number, index: number) => {
    const material = materiais.find(m => m.id === materialId);
    if (material) {
      const materiaisUtilizados = form.getFieldValue('materiais_utilizados') || [];
      materiaisUtilizados[index] = {
        ...materiaisUtilizados[index],
        valor_unitario_momento: material.valor_unitario
      };
      form.setFieldsValue({ materiais_utilizados: materiaisUtilizados });
    }
  };

  if (loadingData) {
    return <div>Carregando...</div>;
  }

  return (
    <Card title="Cadastro de Atendimento" style={{ maxWidth: 800, margin: '0 auto' }}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          data_hora: dayjs(),
          status: 'realizado',
          materiais_utilizados: [],
          procedimentos: [{}] // Inicializar com um procedimento vazio
        }}
      >
        <Form.Item
          name="cliente_id"
          label="Cliente"
          rules={[{ required: true, message: 'Selecione um cliente' }]}
        >
          <Select placeholder="Selecione o cliente" showSearch>
            {clientes.map(cliente => (
              <Option key={cliente.id} value={cliente.id}>
                {cliente.nome} - {cliente.telefone}
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item label="Procedimento">
          <Form.List name="procedimentos">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <div key={key} style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                    <Form.Item
                      {...restField}
                      name={[name, 'procedimento_id']}
                      rules={[{ required: true, message: 'Selecione um procedimento' }]}
                      style={{ flex: 1, marginBottom: 0, marginRight: 8 }}
                    >
                      <Select 
                        placeholder="Selecione o procedimento" 
                        onChange={(value) => handleProcedimentoChange(value, name)}
                        showSearch
                      >
                        {procedimentos.map(procedimento => (
                          <Option key={procedimento.id} value={procedimento.id}>
                            {procedimento.nome || 'Procedimento sem nome'} - R$ {(procedimento.valor_padrao || 0).toFixed(2)}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                    <Button
                      type="text"
                      icon={<MinusCircleOutlined />}
                      onClick={() => {
                        remove(name);
                        handleProcedimentoRemove(name);
                      }}
                      style={{ marginLeft: 8 }}
                      danger
                    />
                  </div>
                ))}
                <Button
                  type="dashed"
                  onClick={() => {
                    add();
                    handleProcedimentoAdd();
                  }}
                  icon={<PlusOutlined />}
                  style={{ width: '100%' }}
                >
                  Adicionar Procedimento
                </Button>
              </>
            )}
          </Form.List>
        </Form.Item>

        <Form.Item
          name="valor_cobrado"
          label="Valor Cobrado"
          rules={[{ required: true, message: 'Informe o valor cobrado' }]}
        >
          <InputNumber
            prefix="R$"
            placeholder="0,00"
            min={0}
            step={0.01}
            precision={2}
            style={{ width: '100%' }}
          />
        </Form.Item>

        <Form.Item
          name="data_hora"
          label="Data e Hora"
          rules={[{ required: true, message: 'Selecione a data e hora' }]}
        >
          <DatePicker 
            showTime 
            format="DD/MM/YYYY HH:mm"
            style={{ width: '100%' }}
          />
        </Form.Item>

        <Form.Item
          name="observacoes"
          label="Observações"
        >
          <TextArea rows={3} placeholder="Observações sobre o atendimento" />
        </Form.Item>

        <Divider>Materiais Utilizados</Divider>

        <Form.List name="materiais_utilizados">
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Card key={key} size="small" style={{ marginBottom: 16 }}>
                  <Space align="baseline">
                    <Form.Item
                      {...restField}
                      name={[name, 'material_id']}
                      rules={[{ required: true, message: 'Selecione o material' }]}
                    >
                      <MaterialSelector
                        placeholder="Selecione ou digite um material"
                        style={{ width: 200 }}
                        onChange={(value) => handleMaterialChange(value, name)}
                        onMaterialCreated={(novoMaterial) => {
                          // Adicionar o novo material à lista de materiais disponíveis
                          setMateriais(prev => [...prev, novoMaterial]);
                        }}
                      />
                    </Form.Item>

                    <Form.Item
                      {...restField}
                      name={[name, 'quantidade_utilizada']}
                      rules={[{ required: true, message: 'Informe a quantidade' }]}
                    >
                      <InputNumber
                        placeholder="Qtd"
                        min={0}
                        step={0.1}
                        precision={2}
                        style={{ width: 100 }}
                      />
                    </Form.Item>

                    <Form.Item
                      {...restField}
                      name={[name, 'valor_unitario_momento']}
                      rules={[{ required: true, message: 'Informe o valor' }]}
                    >
                      <InputNumber
                        prefix="R$"
                        placeholder="Valor"
                        min={0}
                        step={0.01}
                        precision={2}
                        style={{ width: 120 }}
                      />
                    </Form.Item>

                    <MinusCircleOutlined onClick={() => remove(name)} />
                  </Space>
                </Card>
              ))}

              <Form.Item>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  block
                  icon={<PlusOutlined />}
                >
                  Adicionar Material
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              Salvar Atendimento
            </Button>
            <Button onClick={() => form.resetFields()}>
              Limpar
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default AtendimentoForm; 