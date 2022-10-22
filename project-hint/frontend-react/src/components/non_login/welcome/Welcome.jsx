import React from "react";
import { Link } from "react-router-dom";
import MainIcon from "../../../assets/home/home_main_logo.png";
import {
  DivideLine,
  Title,
  BoldTitle,
  BoldGreenTitle,
  Row,
  Content,
  StartBtn,
  Show1Div,
  Show2Div,
  TemplateBlock,
} from "./welcome.style";
import Navbar from "../non_login_navbar/Navbar";

const Welcome = () => {
  return (
    <>
      <Navbar />
      <div className="content-container">
        <div className="wrapper">
          <TemplateBlock>
            <Row style={{ position: "absolute" }}>
              <Show1Div>
                <DivideLine />
                <Title>성공적인 </Title>
                <Title>투자를 위한</Title>
                <Row>
                  <BoldTitle>투자 정보 플랫폼,</BoldTitle>
                </Row>
                <Row>
                  <BoldGreenTitle>HINT</BoldGreenTitle>
                </Row>
                <Content>
                  언제까지 감으로 투자하실건가요?{"\n"}
                  다양한 투자관련 정보들을 모아놓았습니다.{"\n"}
                  성공적인 투자를 기원합니다!{"\n"}
                </Content>
                <Link to="/auth/signUp">
                  <StartBtn>HINT 가입하기</StartBtn>
                </Link>
                <div>
                  <Link to="/auth/signIn">
                    <StartBtn>로그인하러 가기</StartBtn>
                  </Link>
                </div>
              </Show1Div>
              <Show2Div>
                <img
                  width="800px"
                  height="800px"
                  src={MainIcon}
                  style={{ marginTop: "50px" }}
                />
              </Show2Div>
            </Row>
          </TemplateBlock>
        </div>
      </div>
    </>
  );
};

export default Welcome;
