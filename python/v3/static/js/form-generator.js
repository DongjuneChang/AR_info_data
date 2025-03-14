// Form Generator for Visualization Overrides
class FormGenerator {
    constructor() {
        this.form = document.createElement('form');
        this.form.className = 'visualization-form';
    }

    // Add a color picker field
    addColorPicker(label, id, initialValue) {
        const field = document.createElement('div');
        field.className = 'field';

        const labelElement = document.createElement('label');
        labelElement.textContent = label;
        field.appendChild(labelElement);

        const colorPicker = new ColorPicker(initialValue);
        field.appendChild(colorPicker.element);

        this.form.appendChild(field);
        return colorPicker;
    }

    // Add a range slider field
    addRangeSlider(label, id, min, max, step, initialValue) {
        const field = document.createElement('div');
        field.className = 'field';

        const labelElement = document.createElement('label');
        labelElement.textContent = label;
        field.appendChild(labelElement);

        const control = document.createElement('div');
        control.className = 'position-control';

        const slider = document.createElement('input');
        slider.type = 'range';
        slider.id = id;
        slider.min = min;
        slider.max = max;
        slider.step = step;
        slider.value = initialValue;

        const value = document.createElement('span');
        value.id = `${id}-value`;
        value.textContent = initialValue.toFixed(2);

        slider.addEventListener('input', () => {
            value.textContent = parseFloat(slider.value).toFixed(2);
        });

        control.appendChild(slider);
        control.appendChild(value);
        field.appendChild(control);

        this.form.appendChild(field);
        return slider;
    }

    // Add a select field
    addSelect(label, id, options) {
        const field = document.createElement('div');
        field.className = 'field';

        const labelElement = document.createElement('label');
        labelElement.textContent = label;
        field.appendChild(labelElement);

        const select = document.createElement('select');
        select.id = id;

        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.label;
            select.appendChild(optionElement);
        });

        field.appendChild(select);
        this.form.appendChild(field);
        return select;
    }

    // Get the form element
    getForm() {
        return this.form;
    }
}
