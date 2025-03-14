class ColorPicker {
    constructor(initialColor = { r: 1.0, g: 1.0, b: 1.0, a: 1.0 }) {
        this.element = document.createElement('div');
        this.element.className = 'color-picker';
        
        // Create color input
        this.colorInput = document.createElement('input');
        this.colorInput.className = 'color-input';
        this.colorInput.type = 'text';
        this.colorInput.value = this.colorToHex(initialColor);
        
        // Create color preview
        this.colorPreview = document.createElement('div');
        this.colorPreview.className = 'color-preview';
        this.updatePreview(initialColor);
        
        // Create RGBA sliders
        this.rSlider = this.createSlider('R', initialColor.r);
        this.gSlider = this.createSlider('G', initialColor.g);
        this.bSlider = this.createSlider('B', initialColor.b);
        this.aSlider = this.createSlider('A', initialColor.a);
        
        // Add event listeners
        this.colorInput.addEventListener('change', () => {
            const color = this.hexToColor(this.colorInput.value);
            this.updateSliders(color);
            this.updatePreview(color);
        });
        
        // Add elements to container
        this.element.appendChild(this.colorInput);
        this.element.appendChild(this.colorPreview);
        this.element.appendChild(this.rSlider.container);
        this.element.appendChild(this.gSlider.container);
        this.element.appendChild(this.bSlider.container);
        this.element.appendChild(this.aSlider.container);
    }
    
    createSlider(label, initialValue) {
        const container = document.createElement('div');
        container.style.marginTop = '10px';
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.gap = '10px';
        
        const labelElement = document.createElement('label');
        labelElement.textContent = label;
        labelElement.style.width = '20px';
        
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = label === 'A' ? '1' : '255';  // Alpha는 0~1, RGB는 0~255
        slider.step = label === 'A' ? '0.01' : '1';
        slider.value = label === 'A' ? initialValue : Math.round(initialValue * 255);
        slider.style.flex = '1';
        
        const value = document.createElement('span');
        value.textContent = label === 'A' ? initialValue.toFixed(2) : Math.round(initialValue * 255);
        value.style.width = '40px';
        value.style.textAlign = 'right';
        
        slider.addEventListener('input', () => {
            const val = parseFloat(slider.value);
            value.textContent = label === 'A' ? val.toFixed(2) : Math.round(val);
            this.updatePreview(this.getValue());
            this.colorInput.value = this.colorToHex(this.getValue());
        });
        
        container.appendChild(labelElement);
        container.appendChild(slider);
        container.appendChild(value);
        
        return { container, slider, value };
    }
    
    updateSliders(color) {
        this.rSlider.slider.value = Math.round(color.r * 255);
        this.gSlider.slider.value = Math.round(color.g * 255);
        this.bSlider.slider.value = Math.round(color.b * 255);
        this.aSlider.slider.value = color.a;
        
        this.rSlider.value.textContent = Math.round(color.r * 255);
        this.gSlider.value.textContent = Math.round(color.g * 255);
        this.bSlider.value.textContent = Math.round(color.b * 255);
        this.aSlider.value.textContent = color.a.toFixed(2);
    }
    
    updatePreview(color) {
        const r = Math.round(color.r * 255);
        const g = Math.round(color.g * 255);
        const b = Math.round(color.b * 255);
        this.colorPreview.style.backgroundColor = `rgba(${r}, ${g}, ${b}, ${color.a})`;
    }
    
    getValue() {
        return {
            r: parseFloat(this.rSlider.slider.value) / 255,
            g: parseFloat(this.gSlider.slider.value) / 255,
            b: parseFloat(this.bSlider.slider.value) / 255,
            a: parseFloat(this.aSlider.slider.value)
        };
    }
    
    colorToHex(color) {
        const toHex = (n) => {
            const hex = Math.round(n * 255).toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        };
        return `#${toHex(color.r)}${toHex(color.g)}${toHex(color.b)}`;
    }
    
    hexToColor(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16) / 255,
            g: parseInt(result[2], 16) / 255,
            b: parseInt(result[3], 16) / 255,
            a: parseFloat(this.aSlider.slider.value)
        } : null;
    }
}
