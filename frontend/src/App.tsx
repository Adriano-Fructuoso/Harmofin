import React, { useState } from 'react';
import { Layout, Menu, Button, Typography, Space } from 'antd';
import { UserOutlined, CalendarOutlined, HomeOutlined, InboxOutlined, MedicineBoxOutlined } from '@ant-design/icons';
import Clientes from './pages/Clientes';
import Atendimentos from './pages/Atendimentos';
import Materiais from './pages/Materiais';
import Procedimentos from './pages/Procedimentos';
import 'antd/dist/reset.css';

const { Header, Content, Sider } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const [selectedPage, setSelectedPage] = useState<'home' | 'clientes' | 'atendimentos' | 'materiais' | 'procedimentos'>('home');

  const menuItems = [
    {
      key: 'home',
      icon: <HomeOutlined />,
      label: 'Início',
    },
    {
      key: 'clientes',
      icon: <UserOutlined />,
      label: 'Clientes',
    },
    {
      key: 'procedimentos',
      icon: <MedicineBoxOutlined />,
      label: 'Procedimentos',
    },
    {
      key: 'atendimentos',
      icon: <CalendarOutlined />,
      label: 'Atendimentos',
    },
    {
      key: 'materiais',
      icon: <InboxOutlined />,
      label: 'Controle de Estoque',
    },
  ];

  const renderContent = () => {
    switch (selectedPage) {
      case 'clientes':
        return <Clientes />;
      case 'procedimentos':
        return <Procedimentos />;
      case 'atendimentos':
        return <Atendimentos />;
      case 'materiais':
        return <Materiais />;
      default:
        return (
          <div style={{ padding: '50px', textAlign: 'center' }}>
            <Title level={2}>Sistema de Gestão de Clínicas de Harmonização</Title>
            <p>Bem-vindo ao sistema! Use o menu lateral para navegar entre as funcionalidades.</p>
            <div style={{ marginTop: '30px' }}>
              <Button 
                type="primary" 
                size="large" 
                icon={<UserOutlined />}
                onClick={() => setSelectedPage('clientes')}
                style={{ marginRight: '16px' }}
              >
                Gerenciar Clientes
              </Button>
              <Button 
                type="primary" 
                size="large" 
                icon={<MedicineBoxOutlined />}
                onClick={() => setSelectedPage('procedimentos')}
                style={{ marginRight: '16px' }}
              >
                Gerenciar Procedimentos
              </Button>
              <Button 
                type="primary" 
                size="large" 
                icon={<CalendarOutlined />}
                onClick={() => setSelectedPage('atendimentos')}
                style={{ marginRight: '16px' }}
              >
                Gerenciar Atendimentos
              </Button>
              <Button 
                type="primary" 
                size="large" 
                icon={<InboxOutlined />}
                onClick={() => setSelectedPage('materiais')}
              >
                Controle de Estoque
              </Button>
            </div>
          </div>
        );
    }
  };

  const getPageTitle = () => {
    switch (selectedPage) {
      case 'clientes':
        return 'Gestão de Clientes';
      case 'procedimentos':
        return 'Gestão de Procedimentos';
      case 'atendimentos':
        return 'Gestão de Atendimentos';
      case 'materiais':
        return 'Controle de Estoque';
      default:
        return 'Início';
    }
  };

  const getNavigationButtons = () => {
    switch (selectedPage) {
      case 'clientes':
        return (
          <Space>
            <Button 
              type="primary" 
              icon={<CalendarOutlined />}
              onClick={() => setSelectedPage('atendimentos')}
            >
              Ir para Atendimentos
            </Button>
            <Button 
              type="primary" 
              icon={<InboxOutlined />}
              onClick={() => setSelectedPage('materiais')}
            >
              Ir para Estoque
            </Button>
          </Space>
        );
      case 'atendimentos':
        return (
          <Space>
            <Button 
              type="primary" 
              icon={<UserOutlined />}
              onClick={() => setSelectedPage('clientes')}
            >
              Ir para Clientes
            </Button>
            <Button 
              type="primary" 
              icon={<InboxOutlined />}
              onClick={() => setSelectedPage('materiais')}
            >
              Ir para Estoque
            </Button>
          </Space>
        );
      case 'materiais':
        return (
          <Space>
            <Button 
              type="primary" 
              icon={<UserOutlined />}
              onClick={() => setSelectedPage('clientes')}
            >
              Ir para Clientes
            </Button>
            <Button 
              type="primary" 
              icon={<CalendarOutlined />}
              onClick={() => setSelectedPage('atendimentos')}
            >
              Ir para Atendimentos
            </Button>
          </Space>
        );
      default:
        return null;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={250} theme="dark">
        <div style={{ 
          height: '64px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          borderBottom: '1px solid #303030'
        }}>
          <Title level={4} style={{ color: 'white', margin: 0 }}>
            Harmofin
          </Title>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedPage]}
          items={menuItems}
          onClick={({ key }) => setSelectedPage(key as any)}
          style={{ borderRight: 0 }}
        />
      </Sider>
      <Layout>
        <Header style={{ 
          background: '#fff', 
          padding: '0 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <Title level={4} style={{ margin: 0 }}>
            {getPageTitle()}
          </Title>
          <div>
            {getNavigationButtons()}
          </div>
        </Header>
        <Content style={{ margin: 0, background: '#f0f2f5' }}>
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
};

export default App; 