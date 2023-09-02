import React, { useState }  from 'react';
import './index.css';
import FunctionBlock from '../FunctionBlock';
import ChartComponent from '../../ChartComponent';

function MainContent() {
  // 例如，可以根据需要生成多个功能方块
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [currentModal, setCurrentModal] = useState("");
  const blocks = [
    { label: '功能1', name_modal: "modal1", onClick: () => setCurrentModal("modal1")},
    // { label: '功能2', onClick: () => history.push('/feature2') },
    // { label: '功能3', onClick: () => history.push('/feature3') },
    // ... 其他功能方块
  ];

  const closeModal = () => {
    setModalIsOpen(false);
    setCurrentModal("");
  }

  const renderModal = () => {
    switch (currentModal) {
      case "modal1":
        return <ChartComponent isOpen={modalIsOpen} onRequestClose={closeModal} />
      default:
        return null
    }
  }

  return (
    <div className="main-content">
      {blocks.map((bloc, index) => (
        <FunctionBlock key={index} {...bloc} />
      ))}
      {renderModal()}
    </div>
  );
}

export default MainContent;
