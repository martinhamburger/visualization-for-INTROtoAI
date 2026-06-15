from manim import *


class FormWeightedLoss(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"Form-aware Weighted Loss", font_size=70, color=YELLOW).to_edge(UP)
        formula = MathTex(
            r"\mathcal{L}_{\mathrm{form}}",
            r"=",
            r"\frac{",
            r"\sum_{b,t}",
            r"w_{b,t}",
            r"\ell_{b,t}",
            r"}{",
            r"\sum_{b,t}",
            r"w_{b,t}",
            r"}",
            r"=",
            r"\frac{",
            r"\sum_{b,t}",
            r"w_{b,t}",
            r"\left[-\log p_{b,t}(y_{b,t})\right]",
            r"}{",
            r"\sum_{b,t}",
            r"w_{b,t}",
            r"}",
            font_size=46,
        )
        formula[0].set_color(BLUE_A)
        formula.shift(UP * 0.65)
        formula.scale_to_fit_width(13.2)

        token_loss = formula[14]

        loss_box = SurroundingRectangle(token_loss, color=BLUE_A, buff=0.1)
        loss_label = Tex(r"Per-token Cross Entropy", font_size=40, color=BLUE_A)
        loss_label.next_to(loss_box, UP, buff=0.62).shift(LEFT * 0.4)
        loss_arrow = Arrow(loss_label.get_bottom(), loss_box.get_top(), buff=0.08, color=BLUE_A)

        self.play(FadeIn(title, shift=DOWN), Write(formula), run_time=1.8)
        self.play(Create(loss_box), GrowArrow(loss_arrow), FadeIn(loss_label, shift=UP))
        self.play(Indicate(token_loss, color=BLUE_A, scale_factor=1.03))

        weight_box = SurroundingRectangle(formula[8], color=YELLOW, buff=0.06)

        weight_rows = VGroup(
            Tex(r"$2$", r" if token is ", r"$\vert$", r" (line break)", font_size=36),
            Tex(r"$2$", r" if token is ", r"$/$", r" (half-poem separator)", font_size=36),
            Tex(r"$3$", r" if token is ", r"$@$", r" (full poem end)", font_size=36),
            Tex(r"$1$", r" otherwise", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        weight_rows[0][2].set_color(TEAL_A)
        weight_rows[1][2].set_color(ORANGE)
        weight_rows[2][2].set_color(RED_A)
        weight_rows[3][1].set_color(GREY_A)

        case_brace = Brace(weight_rows, LEFT, color=YELLOW)
        weight_name = MathTex(r"w_{b,t}=", font_size=38, color=YELLOW)
        weight_name.next_to(case_brace, LEFT, buff=0.16)
        weight_cases = VGroup(weight_name, case_brace, weight_rows)
        weight_cases.next_to(weight_box, DOWN, buff = 0.8)

        weight_arrow = Arrow(
            weight_box.get_bottom(),
            weight_cases.get_top(),
            buff=0.12,
            color=YELLOW,
        )

        self.play(
            Create(weight_box),
            GrowArrow(weight_arrow),
            FadeIn(weight_cases, shift=UP),
        )

        denominators = VGroup(
            VGroup(formula[16], formula[17]),
        )
        denominator_boxes = VGroup(
            *[SurroundingRectangle(part, color=GREEN_A, buff=0.08) for part in denominators]
        )
        denominator_label = Tex(r"Normalized by Total Weight", font_size=40, color=GREEN_A)
        denominator_label.next_to(denominator_boxes, DOWN, buff=0.62).shift(RIGHT * 0.4)
        denominator_arrow = Arrow(
            denominator_label.get_top(),
            denominators[-1].get_bottom(),
            buff=0.08,
            color=GREEN_A,
        )
        self.play(
            Create(denominator_boxes),
            GrowArrow(denominator_arrow),
            FadeIn(denominator_label, shift=UP),
        )
        self.play(Indicate(denominators, color=GREEN_A, scale_factor=1.03))
        self.wait(1.5)


class ProsodyEmbeddingAndLoss(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"Prosody Embeddings and Auxiliary Heads", font_size=70, color=YELLOW)
        title.to_edge(UP, buff=0.25)

        embedding = MathTex(
            r"x_{b,t}",
            r"=",
            r"E_{\mathrm{token}}(y_{b,t})",
            r"+",
            r"E_{\mathrm{pos}}(t)",
            r"+",
            r"E_{\mathrm{tone}}(\tau_{b,t})",
            r"+",
            r"E_{\mathrm{rhyme}}(\rho_{b,t})",
            font_size=50,
        )
        embedding.next_to(title, DOWN, buff=0.6)
        tone_embedding = embedding[6]
        rhyme_embedding = embedding[8]
        tone_embedding.set_color(TEAL_A)
        rhyme_embedding.set_color(PURPLE_A)

        self.play(FadeIn(title, shift=DOWN), Write(embedding))
        self.play(
            Circumscribe(tone_embedding, color=TEAL_A),
            Circumscribe(rhyme_embedding, color=PURPLE_A),
        )

        hidden = MathTex(r"head_{b,t}", font_size=60, color=WHITE)
        head_specs = [
            (r"\mathrm{LM}", r"\ell_{b,t}", BLUE_A),
            (r"\mathrm{Tone}", r"a_{b,t}\in\mathbb{R}^{4}", TEAL_A),
            (r"\mathrm{Rhyme}", r"r_{b,t}\in\mathbb{R}^{C_{\mathrm{rhyme}}}", PURPLE_A),
        ]
        heads = VGroup()
        outputs = VGroup()
        arrows = VGroup()
        head_colors = []
        for _index, (label, output_tex, color) in enumerate(head_specs):
            head = MathTex(label, font_size=40, color=color)
            box = SurroundingRectangle(head, color=color, buff=0.16, corner_radius=0.08)
            head_group = VGroup(box, head)
            output = MathTex(output_tex, font_size=40, color=color)
            heads.add(head_group)
            outputs.add(output)
            head_colors.append(color)

        # 三个 head 等间距纵向排列，左边缘对齐
        heads.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        heads.move_to(LEFT * 0.2)

        # 三个输出公式分别放在对应 head 右边，左边缘互相对齐
        for i, output in enumerate(outputs):
            output.next_to(heads[i], RIGHT, buff=0.55)
        outputs.align_to(outputs[0], LEFT)

        # h_{b,t} 放在 heads 左侧，纵向与 heads 组中心对齐
        hidden.move_to(LEFT * 3.5)
        hidden.set_y(heads.get_center()[1])

        # 箭头从 hidden 指向每个 head
        for i in range(len(heads)):
            arrows.add(Arrow(
                hidden.get_right(), heads[i].get_left(), buff=0.12, color=head_colors[i]
            ))

        self.play(FadeIn(hidden), LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15))
        self.play(
            LaggedStart(*[FadeIn(head, shift=RIGHT * 0.1) for head in heads], lag_ratio=0.15),
            LaggedStart(*[Write(output) for output in outputs], lag_ratio=0.15),
        )

        total_loss = MathTex(
            r"\mathcal{L}_{\mathrm{total}}",
            r"=",
            r"\mathcal{L}_{\mathrm{form}}",
            r"+",
            r"\lambda",
            r"\left(",
            r"\mathcal{L}_{\mathrm{tone}}",
            r"+",
            r"\mathcal{L}_{\mathrm{rhyme}}",
            r"\right)",
            font_size=60,
        )
        total_loss[0].set_color(YELLOW)
        total_loss[2].set_color(BLUE_A)
        total_loss[4].set_color(ORANGE)
        total_loss[6].set_color(TEAL_A)
        total_loss[8].set_color(PURPLE_A)
        total_loss.to_edge(DOWN, buff=0.6)
        lambda_note = MathTex(r"\lambda=0.1", font_size=38, color=ORANGE)
        lambda_note.next_to(total_loss[4], UP, buff=0.28)

        self.play(Write(total_loss), FadeIn(lambda_note, shift=UP))
        self.play(
            Circumscribe(total_loss[2], color=BLUE_A),
            Circumscribe(total_loss[6], color=TEAL_A),
            Circumscribe(total_loss[8], color=PURPLE_A),
        )
        self.wait(1.5)


class ThemeLoRA(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"Theme Adaptation with LoRA", font_size=70, color=YELLOW).to_edge(UP, buff=0.25)
        embedding = MathTex(
            r"x_{b,t}",
            r"=",
            r"E_{\mathrm{token}}",
            r"+",
            r"E_{\mathrm{pos}}",
            r"+",
            r"E_{\mathrm{tone}}",
            r"+",
            r"E_{\mathrm{rhyme}}",
            r"+",
            r"E_{\mathrm{theme}}",
            font_size=50,
        )
        embedding.to_edge(UP, buff=1.05)
        theme_part = embedding[10]
        theme_part.set_color(PURPLE_A)
        theme_label = MathTex(r"\mathrm{Trainable}", font_size=30, color=PURPLE_A)
        theme_label.next_to(theme_part, DOWN, buff=0.2)
        theme_arrow = Arrow(theme_label.get_top(), theme_part.get_bottom(), buff=0.05, color=PURPLE_A)

        self.play(FadeIn(title, shift=DOWN), Write(embedding))
        self.play(
            Circumscribe(theme_part, color=PURPLE_A),
            GrowArrow(theme_arrow),
            FadeIn(theme_label, shift=UP),
        )

        lora_formula = MathTex(
            r"W'",
            r"=",
            r"W",
            r"+",
            r"\frac{\alpha}{r}",
            r"B",
            r"A",
            font_size=60,
        )
        lora_formula.shift(UP * 1.05)
        lora_formula[0].set_color(WHITE)
        lora_formula[2].set_color(GREY_B)
        lora_formula[5].set_color(GREEN_A)
        lora_formula[6].set_color(YELLOW)

        frozen_label = MathTex(r"\mathrm{Frozen}", font_size=30, color=GREY_B)
        frozen_label.next_to(lora_formula[2], UP, buff=0.3)
        frozen_arrow = Arrow(frozen_label.get_bottom(), lora_formula[2].get_top(), buff=0.06, color=GREY_B)
        trainable_label = MathTex(r"\mathrm{Trainable}", font_size=30, color=GREEN_A)
        trainable_label.next_to(VGroup(lora_formula[5], lora_formula[6]), UP, buff=0.3)
        trainable_arrow = Arrow(
            trainable_label.get_bottom(),
            VGroup(lora_formula[5], lora_formula[6]).get_top(),
            buff=0.06,
            color=GREEN_A,
        )

        self.play(Write(lora_formula))
        self.play(
            Circumscribe(lora_formula[2], color=GREY_B),
            GrowArrow(frozen_arrow),
            FadeIn(frozen_label, shift=UP),
        )
        self.play(
            Circumscribe(VGroup(lora_formula[5], lora_formula[6]), color=GREEN_A),
            GrowArrow(trainable_arrow),
            FadeIn(trainable_label, shift=UP),
        )

        # LoRA's low-rank update: B is tall and narrow, A is short and wide.
        def grid_matrix(rows, cols, color, cell_size=0.34):
            cells = VGroup(
                *[
                    Square(
                        side_length=cell_size,
                        stroke_color=color,
                        stroke_width=1.4,
                        fill_color=color,
                        fill_opacity=0.12,
                    )
                    for _ in range(rows * cols)
                ]
            )
            cells.arrange_in_grid(rows=rows, cols=cols, buff=0)
            border = SurroundingRectangle(cells, color=color, buff=0, stroke_width=2.4)
            return VGroup(cells, border)

        b_matrix = grid_matrix(rows=7, cols=2, color=GREEN_A)
        a_matrix = grid_matrix(rows=2, cols=8, color=YELLOW)
        multiply = MathTex(r"\times", font_size=48, color=WHITE)
        matrix_product = VGroup(b_matrix, multiply, a_matrix).arrange(RIGHT, buff=0.42)
        matrix_product.shift(DOWN * 1.05)

        b_label = MathTex(r"B", font_size=50, color=GREEN_A).next_to(b_matrix, UP, buff=0.18)
        a_label = MathTex(r"A", font_size=50, color=YELLOW).next_to(a_matrix, UP, buff=0.18)
        b_dimension = MathTex(
            r"d_{\mathrm{out}}\times r",
            font_size=40,
            color=GREEN_A,
        ).next_to(b_matrix, DOWN, buff=0.22)
        a_dimension = MathTex(
            r"r\times d_{\mathrm{in}}",
            font_size=40,
            color=YELLOW,
        ).next_to(a_matrix, DOWN, buff=0.22)

        self.play(
            LaggedStart(
                Create(b_matrix),
                Write(multiply),
                Create(a_matrix),
                lag_ratio=0.2,
            ),
            FadeIn(b_label, shift=DOWN),
            FadeIn(a_label, shift=DOWN),
        )
        self.play(Write(b_dimension), Write(a_dimension))

        low_rank = MathTex(
            r"r\ll\min(d_{\mathrm{in}},d_{\mathrm{out}})",
            font_size=40,
            color=WHITE,
        )
        low_rank.to_edge(DOWN, buff=0.5)

        self.play(Write(low_rank))
        self.play(
            Circumscribe(b_matrix, color=GREEN_A),
            Circumscribe(a_matrix, color=YELLOW),
        )
        self.wait(1.5)
