import React from 'react';
import { Form, Input, Button, Space } from 'antd';
import { ClienteCreate } from '../types/atendimento';

const { TextArea } = Input;

interface ClienteFormProps {
  onSubmit: (values: ClienteCreate) => void;
  loading?: boolean;
  initialValues?: Partial<ClienteCreate>;
}

const ClienteForm: React.FC<ClienteFormProps> = ({ 
  onSubmit, 
  loading = false, 
  initialValues 
}) => {
  const [form] = Form.useForm();

  const handleSubmit = (values: ClienteCreate) => {
    onSubmit(values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={initialValues}
    >
      <Form.Item
        name="nome"
        label="Nome"
        rules={[{ required: true, message: 'Por favor, insira o nome' }]}
      >
        <Input placeholder="Nome completo" />
      </Form.Item>

      <Form.Item
        name="telefone"
        label="Telefone"
        rules={[{ required: true, message: 'Por favor, insira o telefone' }]}
      >
        <Input placeholder="(11) 99999-9999" />
      </Form.Item>

      <Form.Item
        name="email"
        label="Email"
        rules={[
          { type: 'email', message: 'Por favor, insira um email válido' }
        ]}
      >
        <Input placeholder="email@exemplo.com" />
      </Form.Item>

      <Form.Item
        name="observacao"
        label="Observação"
      >
        <TextArea rows={3} placeholder="Observações sobre o cliente" />
      </Form.Item>

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            Salvar
          </Button>
          <Button onClick={() => form.resetFields()}>
            Limpar
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default ClienteForm; 