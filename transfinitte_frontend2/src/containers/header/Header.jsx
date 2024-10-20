import React from 'react'
import "./header.css"
import people from "../../assets/people.png"
import ai from "../../assets/ai.png"

const Header = () => {
  return (
    <div className="gpt3__header section_padding" id='home'>
      <div className="gpt3__header-content">
        <h1 className="gradient__text">Let&apos;s Create Extraordinary Innovations with AI</h1>
        <p>Together, we can push the boundaries of creativity, develop groundbreaking applications, and enhance user experiences across various domains. Let’s harness the power of AI to build something remarkable that transforms ideas into reality!.</p>

        <div className="gpt3__header-content__input">
          <input type="email" placeholder="Your Email Address" />
          <button type="button">Get Started</button>
        </div>

        <div className="gpt3__header-content__people">
          
        </div>

      </div>
      <div className="gpt3__header-image">
        <img src={ai} alt="AI" />
      </div>
    </div>
  )
}

export default Header