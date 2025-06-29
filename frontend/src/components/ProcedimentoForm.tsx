import React, { useState, useEffect } from 'react';
import { Form, Input, InputNumber, Switch, Button, Card, Space, Divider, message, Select } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { ProcedimentoCreate, Material } from '../types/procedimento';
import { materiaisApi } from '../services/api';

const { TextArea } = Input;
const { Option } = Select;

interface ProcedimentoFormProps {
  onSubmit: (values: ProcedimentoCreate) => void;
  loading?: boolean;
  initialValues?: Partial<ProcedimentoCreate>;
}

const ProcedimentoForm: React.FC<ProcedimentoFormProps> = ({ 
  onSubmit, 
  loading = false, 
  initialValues 
}) => {
  const [form] = Form.useForm();
  const [materiais, setMateriais] = useState<Material[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    carregarMateriais();
  }, []);

  // Aplicar initialValues quando eles mudarem (para edição)
  useEffect(() => {
    if (initialValues) {
      form.setFieldsValue({
        ativo: true,
        materiais_padrao: [],
        ...initialValues
      });
    }
  }, [initialValues, form]);

  const carregarMateriais = async () => {
    try {
      setLoadingData(true);
      const response = await materiaisApi.listar({ ativo: true });
      setMateriais(response.data.materiais);
    } catch (error) {
      message.error('Erro ao carregar materiais');
    } finally {
      setLoadingData(false);
    }
  };

  const handleSubmit = (values: any) => {
    console.log('🔍 ProcedimentoForm - handleSubmit chamado com valores:', values);
    
    // Processar materiais padrão para garantir que material_id seja número
    const materiaisPadrao = values.materiais_padrao?.map((mp: any) => {
      console.log('🔧 Processando material padrão:', mp);
      return {
        material_id: typeof mp.material_id === 'string' ? parseInt(mp.material_id) : mp.material_id,
        quantidade_padrao: mp.quantidade_padrao
      };
    }) || [];

    console.log('📦 Materiais padrão processados:', materiaisPadrao);

    const procedimentoData: ProcedimentoCreate = {
      nome: values.nome,
      descricao: values.descricao,
      valor_padrao: values.valor_padrao,
      ativo: values.ativo,
      materiais_padrao: materiaisPadrao
    };
    
    console.log('📤 Dados do procedimento a serem enviados:', procedimentoData);
    onSubmit(procedimentoData);
  };

  if (loadingData) {
    return <div>Carregando...</div>;
  }

  return (
    <Card title="Cadastro de Procedimento" style={{ maxWidth: 800, margin: '0 auto' }}>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          ativo: true,
          materiais_padrao: []
        }}
      >
        <Form.Item
          name="nome"
          label="Nome do Procedimento"
          rules={[{ required: true, message: 'Informe o nome do procedimento' }]}
        >
          <Input placeholder="Ex: Botox, Preenchimento, etc." />
        </Form.Item>

        <Form.Item
          name="descricao"
          label="Descrição"
        >
          <TextArea 
            rows={3} 
            placeholder="Descrição detalhada do procedimento (opcional)" 
          />
        </Form.Item>

        <Form.Item
          name="valor_padrao"
          label="Valor Padrão"
          rules={[{ required: true, message: 'Informe o valor padrão' }]}
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
          name="ativo"
          label="Ativo"
          valuePropName="checked"
        >
          <Switch />
        </Form.Item>

        <Divider>Materiais Padrão</Divider>
        <p style={{ color: '#666', marginBottom: 16 }}>
          Defina os materiais que são utilizados por padrão neste procedimento. 
          Quando um atendimento usar este procedimento, estes materiais serão automaticamente incluídos.
        </p>

        <Form.List name="materiais_padrao">
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
                      <Select
                        placeholder="Selecione o material"
                        style={{ width: 250 }}
                        showSearch
                        filterOption={(input, option) =>
                          (option?.children as unknown as string)?.toLowerCase().includes(input.toLowerCase())
                        }
                      >
                        {materiais.map(material => (
                          <Option key={material.id} value={material.id}>
                            {material.nome} (Estoque: {material.quantidade_disponivel} {material.unidade})
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>

                    <Form.Item
                      {...restField}
                      name={[name, 'quantidade_padrao']}
                      rules={[{ required: true, message: 'Informe a quantidade' }]}
                    >
                      <InputNumber
                        placeholder="Qtd"
                        min={0}
                        step={0.1}
                        precision={2}
                        style={{ width: 120 }}
                      />
                    </Form.Item>

                    <MinusCircleOutlined 
                      onClick={() => remove(name)} 
                      style={{ color: '#ff4d4f', cursor: 'pointer' }}
                    />
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
                  Adicionar Material Padrão
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              Salvar Procedimento
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

export default ProcedimentoForm; 